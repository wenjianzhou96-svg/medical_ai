"""
医疗智能体系统 - 问诊CRUD操作

提供问诊记录、问诊消息、AI报告等数据库操作
"""

from typing import Optional, List
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc

from app.models.consultation import ConsultationRecord, ConsultationMessage, AIReport


class ConsultationCRUD:
    """问诊记录CRUD操作类"""

    @staticmethod
    def get_by_id(db: Session, consultation_id: int) -> Optional[ConsultationRecord]:
        """根据问诊ID获取问诊记录"""
        return db.query(ConsultationRecord).filter(
            ConsultationRecord.consultation_id == consultation_id
        ).first()

    @staticmethod
    def get_by_user(
        db: Session,
        user_id: int,
        skip: int = 0,
        limit: int = 20,
        status: Optional[int] = None
    ) -> tuple[List[ConsultationRecord], int]:
        """获取用户的问诊记录列表"""
        query = db.query(ConsultationRecord).filter(
            ConsultationRecord.user_id == user_id
        )

        if status is not None:
            query = query.filter(ConsultationRecord.status == status)

        total = query.count()
        records = query.order_by(desc(ConsultationRecord.created_at)).offset(skip).limit(limit).all()

        return records, total

    @staticmethod
    def get_list(
        db: Session,
        skip: int = 0,
        limit: int = 20,
        user_id: Optional[int] = None,
        doctor_id: Optional[int] = None,
        status: Optional[int] = None,
        severity_level: Optional[int] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> tuple[List[ConsultationRecord], int]:
        """获取问诊记录列表"""
        query = db.query(ConsultationRecord)

        # 构建过滤条件
        filters = []
        if user_id:
            filters.append(ConsultationRecord.user_id == user_id)
        if doctor_id:
            filters.append(ConsultationRecord.doctor_id == doctor_id)
        if status is not None:
            filters.append(ConsultationRecord.status == status)
        if severity_level is not None:
            filters.append(ConsultationRecord.severity_level == severity_level)

        if filters:
            query = query.filter(and_(*filters))

        # 获取总数
        total = query.count()

        # 分页查询
        records = query.order_by(desc(ConsultationRecord.created_at)).offset(skip).limit(limit).all()

        return records, total

    @staticmethod
    def create(
        db: Session,
        user_id: int,
        title: Optional[str] = None,
        symptoms: Optional[str] = None,
        doctor_id: Optional[int] = None
    ) -> ConsultationRecord:
        """创建问诊记录"""
        consultation = ConsultationRecord(
            user_id=user_id,
            title=title,
            symptoms=symptoms,
            doctor_id=doctor_id,
            status=0,  # 进行中
            conversation_history=[]
        )
        db.add(consultation)
        db.commit()
        db.refresh(consultation)
        return consultation

    @staticmethod
    def update(
        db: Session,
        consultation: ConsultationRecord,
        **kwargs
    ) -> ConsultationRecord:
        """更新问诊记录"""
        for key, value in kwargs.items():
            if value is not None and hasattr(consultation, key):
                setattr(consultation, key, value)
        db.commit()
        db.refresh(consultation)
        return consultation

    @staticmethod
    def add_message(
        db: Session,
        consultation_id: int,
        sender_type: str,
        content: str,
        sender_id: Optional[int] = None,
        message_metadata: Optional[dict] = None
    ) -> ConsultationMessage:
        """添加问诊消息"""
        message = ConsultationMessage(
            consultation_id=consultation_id,
            sender_type=sender_type,
            sender_id=sender_id,
            content=content,
            message_metadata=message_metadata
        )
        db.add(message)

        # 更新问诊记录的对话历史
        consultation = ConsultationCRUD.get_by_id(db, consultation_id)
        if consultation:
            history = consultation.conversation_history or []
            history.append({
                "sender_type": sender_type,
                "sender_id": sender_id,
                "content": content,
                "created_at": datetime.utcnow().isoformat()
            })
            consultation.conversation_history = history

        db.commit()
        db.refresh(message)
        return message

    @staticmethod
    def get_messages(
        db: Session,
        consultation_id: int,
        skip: int = 0,
        limit: int = 50
    ) -> List[ConsultationMessage]:
        """获取问诊消息列表"""
        return db.query(ConsultationMessage).filter(
            ConsultationMessage.consultation_id == consultation_id
        ).order_by(ConsultationMessage.created_at).offset(skip).limit(limit).all()

    @staticmethod
    def complete(
        db: Session,
        consultation_id: int,
        ai_suggestion: Optional[str] = None
    ) -> ConsultationRecord:
        """完成问诊"""
        consultation = ConsultationCRUD.get_by_id(db, consultation_id)
        if not consultation:
            return None

        consultation.status = 1  # 已完成
        if ai_suggestion:
            consultation.ai_suggestion = ai_suggestion

        db.commit()
        db.refresh(consultation)
        return consultation

    @staticmethod
    def cancel(db: Session, consultation_id: int) -> Optional[ConsultationRecord]:
        """取消问诊"""
        consultation = ConsultationCRUD.get_by_id(db, consultation_id)
        if not consultation:
            return None

        consultation.status = 2  # 已取消
        db.commit()
        db.refresh(consultation)
        return consultation

    @staticmethod
    def delete(db: Session, consultation_id: int) -> bool:
        """删除问诊记录"""
        consultation = ConsultationCRUD.get_by_id(db, consultation_id)
        if consultation:
            db.delete(consultation)
            db.commit()
            return True
        return False


class ConsultationMessageCRUD:
    """问诊消息CRUD操作类"""

    @staticmethod
    def get_by_id(db: Session, message_id: int) -> Optional[ConsultationMessage]:
        """根据消息ID获取消息"""
        return db.query(ConsultationMessage).filter(
            ConsultationMessage.message_id == message_id
        ).first()

    @staticmethod
    def get_by_consultation(
        db: Session,
        consultation_id: int,
        skip: int = 0,
        limit: int = 50
    ) -> List[ConsultationMessage]:
        """获取问诊的所有消息"""
        return db.query(ConsultationMessage).filter(
            ConsultationMessage.consultation_id == consultation_id
        ).order_by(ConsultationMessage.created_at).offset(skip).limit(limit).all()

    @staticmethod
    def delete(db: Session, message_id: int) -> bool:
        """删除消息"""
        message = ConsultationMessageCRUD.get_by_id(db, message_id)
        if message:
            db.delete(message)
            db.commit()
            return True
        return False


class AIReportCRUD:
    """AI报告CRUD操作类"""

    @staticmethod
    def get_by_id(db: Session, report_id: int) -> Optional[AIReport]:
        """根据报告ID获取报告"""
        return db.query(AIReport).filter(AIReport.report_id == report_id).first()

    @staticmethod
    def get_by_consultation(
        db: Session,
        consultation_id: int
    ) -> List[AIReport]:
        """获取问诊的所有报告"""
        return db.query(AIReport).filter(
            AIReport.consultation_id == consultation_id
        ).order_by(desc(AIReport.created_at)).all()

    @staticmethod
    def create(
        db: Session,
        consultation_id: int,
        user_id: int,
        report_type: str = 'text',
        report_content: Optional[dict] = None,
        report_file_url: Optional[str] = None
    ) -> AIReport:
        """创建AI报告"""
        report = AIReport(
            consultation_id=consultation_id,
            user_id=user_id,
            report_type=report_type,
            report_content=report_content,
            report_file_url=report_file_url
        )
        db.add(report)
        db.commit()
        db.refresh(report)
        return report

    @staticmethod
    def delete(db: Session, report_id: int) -> bool:
        """删除报告"""
        report = AIReportCRUD.get_by_id(db, report_id)
        if report:
            db.delete(report)
            db.commit()
            return True
        return False
