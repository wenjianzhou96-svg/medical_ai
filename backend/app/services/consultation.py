"""
医疗智能体系统 - 问诊服务层

提供问诊会话、AI对话、诊断建议等业务逻辑
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session

from app.models.consultation import ConsultationRecord
from app.crud.consultation import ConsultationCRUD, AIReportCRUD
from app.services.ai import AIService, get_ai_service
from app.core.exceptions import NotFoundException, BadRequestException, ServiceUnavailableException
from app.core.logging import logger


class ConsultationService:
    """问诊服务类"""

    def __init__(self, db: Session):
        """初始化问诊服务"""
        self.db = db
        self.consultation_crud = ConsultationCRUD()
        self.report_crud = AIReportCRUD()
        # 使用延迟初始化获取 AI 服务实例
        self.ai_service = get_ai_service()

    async def create_consultation(
        self,
        user_id: int,
        title: Optional[str] = None,
        symptoms: Optional[str] = None,
        doctor_id: Optional[int] = None
    ) -> ConsultationRecord:
        """
        创建问诊会话

        Args:
            user_id: 用户ID
            title: 问诊标题
            symptoms: 初始症状描述
            doctor_id: 医生ID（可选）

        Returns:
            问诊记录对象
        """
        # 创建问诊记录
        consultation = self.consultation_crud.create(
            db=self.db,
            user_id=user_id,
            title=title,
            symptoms=symptoms,
            doctor_id=doctor_id
        )

        # 如果有初始症状，触发AI回复
        if symptoms:
            # 添加用户消息
            self.consultation_crud.add_message(
                db=self.db,
                consultation_id=consultation.consultation_id,
                sender_type="user",
                content=symptoms,
                sender_id=user_id
            )

            # 尝试调用AI获取回复，如果失败则记录日志但不阻塞流程
            try:
                ai_result = await self.ai_service.consultation_chat(
                    user_message=symptoms,
                    conversation_history=[],
                    user_info=None
                )

                # 添加AI消息
                self.consultation_crud.add_message(
                    db=self.db,
                    consultation_id=consultation.consultation_id,
                    sender_type="ai",
                    content=ai_result["reply"]
                )

                # 检查紧急情况
                if ai_result.get("is_emergency"):
                    consultation.severity_level = 3  # 紧急
                    
            except ServiceUnavailableException as e:
                # AI服务不可用，记录日志但继续创建问诊
                logger.warning(f"AI服务暂不可用，问诊创建成功但无AI回复: {str(e)}")
                # 添加系统提示消息
                self.consultation_crud.add_message(
                    db=self.db,
                    consultation_id=consultation.consultation_id,
                    sender_type="ai",
                    content="您好！感谢您的问诊。AI助手暂时无法回复，请稍后再试或直接描述您的症状。"
                )
            except Exception as e:
                # 其他异常，记录日志
                logger.error(f"AI服务调用异常: {str(e)}")
                # 添加系统提示消息
                self.consultation_crud.add_message(
                    db=self.db,
                    consultation_id=consultation.consultation_id,
                    sender_type="ai",
                    content="您好！感谢您的问诊。系统暂时繁忙，请稍后再试。"
                )

            self.db.commit()
            self.db.refresh(consultation)

        return consultation

    async def send_message(
        self,
        consultation_id: int,
        user_id: int,
        message: str,
        user_info: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        发送问诊消息

        Args:
            consultation_id: 问诊ID
            user_id: 用户ID
            message: 消息内容
            user_info: 用户健康信息

        Returns:
            包含AI回复的字典
        """
        # 获取问诊记录
        consultation = self.consultation_crud.get_by_id(self.db, consultation_id)
        if not consultation:
            raise NotFoundException("问诊记录", consultation_id)

        # 检查问诊状态
        if consultation.status not in [0, 3]:  # 进行中 或 待审核
            raise BadRequestException("问诊会话已结束，无法继续发送消息")

        # 添加用户消息
        self.consultation_crud.add_message(
            db=self.db,
            consultation_id=consultation_id,
            sender_type="user",
            content=message,
            sender_id=user_id
        )

        # 获取对话历史
        messages = self._build_conversation_history(consultation.conversation_history)

        # 尝试调用AI获取回复
        ai_reply = "感谢您的消息。AI助手暂时无法回复，请稍后再试。"
        is_emergency = False
        follow_up_questions = []
        
        try:
            ai_result = await self.ai_service.consultation_chat(
                user_message=message,
                conversation_history=messages,
                user_info=user_info
            )
            
            ai_reply = ai_result.get("reply", ai_reply)
            is_emergency = ai_result.get("is_emergency", False)
            follow_up_questions = ai_result.get("follow_up_questions", [])
            
        except ServiceUnavailableException as e:
            logger.warning(f"AI服务暂不可用: {str(e)}")
        except Exception as e:
            logger.error(f"AI服务调用异常: {str(e)}")

        # 添加AI消息
        self.consultation_crud.add_message(
            db=self.db,
            consultation_id=consultation_id,
            sender_type="ai",
            content=ai_reply
        )

        # 更新严重程度
        if is_emergency:
            consultation.severity_level = 3  # 紧急

        # 更新症状描述
        if consultation.symptoms:
            consultation.symptoms += f"\n{message}"
        else:
            consultation.symptoms = message

        self.db.commit()
        self.db.refresh(consultation)

        return {
            "reply": ai_reply,
            "suggestion": "",
            "is_emergency": is_emergency,
            "follow_up_questions": follow_up_questions
        }

    async def finish_consultation(
        self,
        consultation_id: int,
        user_id: int,
        user_info: Optional[Dict[str, Any]] = None
    ) -> ConsultationRecord:
        """
        完成问诊，生成诊断建议

        Args:
            consultation_id: 问诊ID
            user_id: 用户ID
            user_info: 用户健康信息

        Returns:
            完成的问诊记录
        """
        # 获取问诊记录
        consultation = self.consultation_crud.get_by_id(self.db, consultation_id)
        if not consultation:
            raise NotFoundException("问诊记录", consultation_id)

        # 获取对话历史
        messages = self._build_conversation_history(consultation.conversation_history)

        # 生成诊断建议
        diagnosis = await self.ai_service.generate_diagnosis_suggestion(
            symptoms=consultation.symptoms or "",
            conversation_history=messages,
            user_info=user_info
        )

        # 更新问诊记录
        consultation.ai_suggestion = str(diagnosis)
        consultation.status = 3  # 待审核（AI生成诊断建议后自动进入待审核状态）

        # 设置严重程度
        severity_map = {
            "low": 0,
            "medium": 1,
            "high": 2,
            "critical": 3
        }
        severity = diagnosis.get("severity", "low").lower()
        consultation.severity_level = severity_map.get(severity, 0)

        self.db.commit()
        self.db.refresh(consultation)

        return consultation

    async def generate_report(
        self,
        consultation_id: int,
        user_id: int
    ) -> Dict[str, Any]:
        """
        生成问诊报告

        Args:
            consultation_id: 问诊ID
            user_id: 用户ID

        Returns:
            生成的报告内容
        """
        # 获取问诊记录
        consultation = self.consultation_crud.get_by_id(self.db, consultation_id)
        if not consultation:
            raise NotFoundException("问诊记录", consultation_id)

        # 构建问诊数据
        consultation_data = {
            "consultation_id": consultation.consultation_id,
            "title": consultation.title,
            "symptoms": consultation.symptoms,
            "conversation_history": consultation.conversation_history,
            "ai_suggestion": consultation.ai_suggestion,
            "doctor_review": consultation.doctor_review,
            "severity_level": consultation.severity_level,
            "created_at": consultation.created_at.isoformat() if consultation.created_at else None,
            "updated_at": consultation.updated_at.isoformat() if consultation.updated_at else None
        }

        # 调用AI生成报告
        report_content = await self.ai_service.generate_consultation_report(
            consultation_data=consultation_data
        )

        # 保存报告
        report = self.report_crud.create(
            db=self.db,
            consultation_id=consultation_id,
            user_id=user_id,
            report_type="text",
            report_content=report_content
        )

        return report_content

    def get_consultation(
        self,
        consultation_id: int
    ) -> ConsultationRecord:
        """获取问诊详情"""
        consultation = self.consultation_crud.get_by_id(self.db, consultation_id)
        if not consultation:
            raise NotFoundException("问诊记录", consultation_id)
        return consultation

    def get_user_consultations(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 20,
        status: Optional[int] = None
    ) -> tuple[List[ConsultationRecord], int]:
        """获取用户的问诊列表"""
        return self.consultation_crud.get_by_user(
            db=self.db,
            user_id=user_id,
            skip=skip,
            limit=limit,
            status=status
        )

    def get_all_consultations(
        self,
        skip: int = 0,
        limit: int = 20,
        user_id: Optional[int] = None,
        doctor_id: Optional[int] = None,
        status: Optional[int] = None,
        severity_level: Optional[int] = None
    ) -> tuple[List[ConsultationRecord], int]:
        """获取所有问诊列表（管理员/医生用）"""
        return self.consultation_crud.get_list(
            db=self.db,
            skip=skip,
            limit=limit,
            user_id=user_id,
            doctor_id=doctor_id,
            status=status,
            severity_level=severity_level
        )

    def cancel_consultation(
        self,
        consultation_id: int
    ) -> ConsultationRecord:
        """取消问诊"""
        consultation = self.consultation_crud.cancel(self.db, consultation_id)
        if not consultation:
            raise NotFoundException("问诊记录", consultation_id)
        return consultation

    def delete_consultation(self, consultation_id: int) -> None:
        """删除问诊记录（物理删除）"""
        # 先删除关联的消息
        from app.models.consultation import ConsultationMessage, AIReport
        self.db.query(ConsultationMessage).filter(
            ConsultationMessage.consultation_id == consultation_id
        ).delete()
        # 再删除关联的报告
        self.db.query(AIReport).filter(
            AIReport.consultation_id == consultation_id
        ).delete()
        # 最后删除问诊记录
        success = self.consultation_crud.delete(self.db, consultation_id)
        if not success:
            raise NotFoundException("问诊记录", consultation_id)

    def doctor_review(
        self,
        consultation_id: int,
        doctor_id: int,
        review_content: str
    ) -> ConsultationRecord:
        """
        医生审核

        Args:
            consultation_id: 问诊ID
            doctor_id: 医生ID
            review_content: 审核意见

        Returns:
            更新后的问诊记录
        """
        consultation = self.consultation_crud.get_by_id(self.db, consultation_id)
        if not consultation:
            raise NotFoundException("问诊记录", consultation_id)

        consultation.doctor_review = review_content
        consultation.doctor_id = doctor_id

        # 如果AI建议已审核，状态变为已完成
        if consultation.status == 3:  # 待审核
            consultation.status = 1  # 已完成

        self.db.commit()
        self.db.refresh(consultation)

        return consultation

    def _build_conversation_history(
        self,
        conversation_history: Optional[List[Dict]]
    ) -> List[Dict[str, str]]:
        """构建对话历史（适配AI API格式）"""
        if not conversation_history:
            return []

        messages = []
        for msg in conversation_history:
            role = "user" if msg.get("sender_type") == "user" else "assistant"
            messages.append({
                "role": role,
                "content": msg.get("content", "")
            })

        return messages
