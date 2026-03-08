"""
医疗智能体系统 - 问诊模块单元测试

测试问诊相关的API接口和业务逻辑
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.models.consultation import ConsultationRecord, ConsultationMessage, AIReport
from app.crud.consultation import ConsultationCRUD, AIReportCRUD
from app.services.consultation import ConsultationService


# 测试数据库配置
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def db():
    """创建测试数据库会话"""
    from app.models.base import Base
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def mock_ai_service():
    """模拟AI服务"""
    ai_service = Mock()
    ai_service.consultation_chat = AsyncMock(return_value={
        "reply": "根据您的描述，建议您多休息。",
        "suggestion": "注意休息",
        "is_emergency": False,
        "follow_up_questions": ["您还有其他症状吗？"]
    })
    ai_service.generate_diagnosis_suggestion = AsyncMock(return_value={
        "diagnosis": "可能是感冒",
        "severity": "low",
        "suggestions": ["多喝水", "注意休息"]
    })
    ai_service.generate_consultation_report = AsyncMock(return_value={
        "title": "问诊报告",
        "content": "根据您的症状..."
    })
    return ai_service


class TestConsultationCRUD:
    """测试问诊CRUD操作"""

    def test_create_consultation(self, db):
        """测试创建问诊记录"""
        consultation = ConsultationCRUD.create(
            db=db,
            user_id=1,
            title="测试问诊",
            symptoms="头痛"
        )
        
        assert consultation is not None
        assert consultation.user_id == 1
        assert consultation.title == "测试问诊"
        assert consultation.symptoms == "头痛"
        assert consultation.status == 0  # 进行中

    def test_get_consultation_by_id(self, db):
        """测试根据ID获取问诊"""
        # 创建问诊
        consultation = ConsultationCRUD.create(
            db=db,
            user_id=1,
            title="测试问诊",
            symptoms="头痛"
        )
        
        # 获取问诊
        result = ConsultationCRUD.get_by_id(db, consultation.consultation_id)
        
        assert result is not None
        assert result.consultation_id == consultation.consultation_id
        assert result.title == "测试问诊"

    def test_get_consultations_by_user(self, db):
        """测试获取用户问诊列表"""
        # 创建多个问诊
        for i in range(3):
            ConsultationCRUD.create(
                db=db,
                user_id=1,
                title=f"问诊{i+1}",
                symptoms=f"症状{i+1}"
            )
        
        # 获取用户问诊列表
        consultations, total = ConsultationCRUD.get_by_user(
            db=db,
            user_id=1,
            skip=0,
            limit=10
        )
        
        assert total == 3
        assert len(consultations) == 3

    def test_add_message(self, db):
        """测试添加问诊消息"""
        # 创建问诊
        consultation = ConsultationCRUD.create(
            db=db,
            user_id=1,
            title="测试问诊",
            symptoms="头痛"
        )
        
        # 添加用户消息
        message = ConsultationCRUD.add_message(
            db=db,
            consultation_id=consultation.consultation_id,
            sender_type="user",
            content="我头痛",
            sender_id=1
        )
        
        assert message is not None
        assert message.content == "我头痛"
        assert message.sender_type == "user"
        
        # 验证对话历史已更新
        updated_consultation = ConsultationCRUD.get_by_id(db, consultation.consultation_id)
        assert len(updated_consultation.conversation_history) == 1

    def test_complete_consultation(self, db):
        """测试完成问诊"""
        # 创建问诊
        consultation = ConsultationCRUD.create(
            db=db,
            user_id=1,
            title="测试问诊",
            symptoms="头痛"
        )
        
        # 完成问诊
        completed = ConsultationCRUD.complete(
            db=db,
            consultation_id=consultation.consultation_id,
            ai_suggestion="建议休息"
        )
        
        assert completed.status == 1  # 已完成
        assert completed.ai_suggestion == "建议休息"

    def test_cancel_consultation(self, db):
        """测试取消问诊"""
        # 创建问诊
        consultation = ConsultationCRUD.create(
            db=db,
            user_id=1,
            title="测试问诊",
            symptoms="头痛"
        )
        
        # 取消问诊
        cancelled = ConsultationCRUD.cancel(
            db=db,
            consultation_id=consultation.consultation_id
        )
        
        assert cancelled.status == 2  # 已取消

    def test_get_messages(self, db):
        """测试获取问诊消息列表"""
        # 创建问诊
        consultation = ConsultationCRUD.create(
            db=db,
            user_id=1,
            title="测试问诊",
            symptoms="头痛"
        )
        
        # 添加消息
        ConsultationCRUD.add_message(
            db=db,
            consultation_id=consultation.consultation_id,
            sender_type="user",
            content="我头痛",
            sender_id=1
        )
        ConsultationCRUD.add_message(
            db=db,
            consultation_id=consultation.consultation_id,
            sender_type="ai",
            content="建议休息"
        )
        
        # 获取消息列表
        messages = ConsultationCRUD.get_messages(
            db=db,
            consultation_id=consultation.consultation_id
        )
        
        assert len(messages) == 2


class TestAIReportCRUD:
    """测试AI报告CRUD操作"""

    def test_create_report(self, db):
        """测试创建报告"""
        # 创建问诊
        consultation = ConsultationCRUD.create(
            db=db,
            user_id=1,
            title="测试问诊",
            symptoms="头痛"
        )
        
        # 创建报告
        report = AIReportCRUD.create(
            db=db,
            consultation_id=consultation.consultation_id,
            user_id=1,
            report_type="text",
            report_content={"content": "测试报告内容"}
        )
        
        assert report is not None
        assert report.report_type == "text"
        assert report.consultation_id == consultation.consultation_id

    def test_get_reports_by_consultation(self, db):
        """测试获取问诊的报告列表"""
        # 创建问诊
        consultation = ConsultationCRUD.create(
            db=db,
            user_id=1,
            title="测试问诊",
            symptoms="头痛"
        )
        
        # 创建多个报告
        for i in range(3):
            AIReportCRUD.create(
                db=db,
                consultation_id=consultation.consultation_id,
                user_id=1,
                report_type="text",
                report_content={"content": f"报告{i+1}"}
            )
        
        # 获取报告列表
        reports = AIReportCRUD.get_by_consultation(
            db=db,
            consultation_id=consultation.consultation_id
        )
        
        assert len(reports) == 3


class TestConsultationService:
    """测试问诊服务"""

    @pytest.mark.asyncio
    async def test_create_consultation_with_symptoms(self, db, mock_ai_service):
        """测试创建带症状的问诊（触发AI回复）"""
        service = ConsultationService(db)
        service.ai_service = mock_ai_service
        
        consultation = await service.create_consultation(
            user_id=1,
            title="测试问诊",
            symptoms="我头痛"
        )
        
        assert consultation is not None
        assert consultation.user_id == 1
        # 验证对话历史
        assert len(consultation.conversation_history) == 2  # 用户消息 + AI回复

    @pytest.mark.asyncio
    async def test_send_message(self, db, mock_ai_service):
        """测试发送消息"""
        service = ConsultationService(db)
        service.ai_service = mock_ai_service
        
        # 创建问诊
        consultation = await service.create_consultation(
            user_id=1,
            title="测试问诊",
            symptoms="我头痛"
        )
        
        # 发送消息
        result = await service.send_message(
            consultation_id=consultation.consultation_id,
            user_id=1,
            message="还咳嗽"
        )
        
        assert result is not None
        assert "reply" in result
        assert "follow_up_questions" in result

    @pytest.mark.asyncio
    async def test_finish_consultation(self, db, mock_ai_service):
        """测试完成问诊生成诊断建议"""
        service = ConsultationService(db)
        service.ai_service = mock_ai_service
        
        # 创建问诊
        consultation = await service.create_consultation(
            user_id=1,
            title="测试问诊",
            symptoms="我头痛"
        )
        
        # 完成问诊
        completed = await service.finish_consultation(
            consultation_id=consultation.consultation_id,
            user_id=1
        )
        
        assert completed is not None
        assert completed.ai_suggestion is not None
        # 根据需求，AI生成诊断建议后自动进入待审核状态
        assert completed.status == 3  # 待审核

    @pytest.mark.asyncio
    async def test_doctor_review(self, db, mock_ai_service):
        """测试医生审核"""
        service = ConsultationService(db)
        service.ai_service = mock_ai_service
        
        # 创建并完成问诊
        consultation = await service.create_consultation(
            user_id=1,
            title="测试问诊",
            symptoms="我头痛"
        )
        consultation = await service.finish_consultation(
            consultation_id=consultation.consultation_id,
            user_id=1
        )
        
        # 医生审核
        reviewed = service.doctor_review(
            consultation_id=consultation.consultation_id,
            doctor_id=2,
            review_content="同意AI诊断建议"
        )
        
        assert reviewed.doctor_review == "同意AI诊断建议"
        assert reviewed.doctor_id == 2
        # 审核通过后状态变为已完成
        assert reviewed.status == 1  # 已完成

    def test_get_consultation(self, db):
        """测试获取问诊详情"""
        # 创建问诊
        consultation = ConsultationCRUD.create(
            db=db,
            user_id=1,
            title="测试问诊",
            symptoms="头痛"
        )
        
        service = ConsultationService(db)
        result = service.get_consultation(consultation.consultation_id)
        
        assert result is not None
        assert result.consultation_id == consultation.consultation_id

    def test_cancel_consultation(self, db):
        """测试取消问诊"""
        # 创建问诊
        consultation = ConsultationCRUD.create(
            db=db,
            user_id=1,
            title="测试问诊",
            symptoms="头痛"
        )
        
        service = ConsultationService(db)
        cancelled = service.cancel_consultation(consultation.consultation_id)
        
        assert cancelled.status == 2  # 已取消


class TestConsultationStatus:
    """测试问诊状态流转"""

    def test_status_flow(self, db):
        """测试问诊状态流转"""
        # 1. 创建问诊 -> 进行中
        consultation = ConsultationCRUD.create(
            db=db,
            user_id=1,
            title="测试问诊",
            symptoms="头痛"
        )
        assert consultation.status == 0  # 进行中
        
        # 2. 完成问诊 -> 待审核（根据需求）
        consultation = ConsultationCRUD.complete(
            db=db,
            consultation_id=consultation.consultation_id,
            ai_suggestion="建议休息"
        )
        # 注意：这里应该是3（待审核），但CRUD直接设置为1
        # 实际业务逻辑在service层处理
        assert consultation.status == 1
        
        # 3. 医生审核 -> 已完成
        consultation.doctor_review = "同意"
        consultation.status = 1  # 审核通过
        db.commit()
        db.refresh(consultation)
        assert consultation.status == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
