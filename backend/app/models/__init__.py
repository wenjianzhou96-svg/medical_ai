"""
医疗智能体系统 - 数据模型

包含所有数据库模型
"""

from app.models.user import User, Role, Permission, LoginLog
from app.models.doctor import Doctor, Schedule
from app.models.consultation import ConsultationRecord, ConsultationMessage, AIReport
from app.models.health import (
    HealthRecord, 
    VitalSign, 
    MedicationRecord, 
    VaccinationRecord, 
    ExaminationRecord
)
from app.models.content import Category, Article, Comment, Review
from app.models.system import (
    SystemConfig, 
    OperationLog, 
    Notification, 
    AlertRecord, 
    FollowUpPlan, 
    FollowUpRecord
)
from app.models.knowledge import (
    MedicalKnowledge, 
    KnowledgeCategory, 
    DrugInfo, 
    ClinicalGuide
)

__all__ = [
    # 用户相关
    "User",
    "Role",
    "Permission",
    "LoginLog",
    # 医生相关
    "Doctor",
    "Schedule",
    # 问诊相关
    "ConsultationRecord",
    "ConsultationMessage",
    "AIReport",
    # 健康管理相关
    "HealthRecord",
    "VitalSign",
    "MedicationRecord",
    "VaccinationRecord",
    "ExaminationRecord",
    # 内容管理相关
    "Category",
    "Article",
    "Comment",
    "Review",
    # 系统管理相关
    "SystemConfig",
    "OperationLog",
    "Notification",
    "AlertRecord",
    "FollowUpPlan",
    "FollowUpRecord",
    # 知识库相关
    "MedicalKnowledge",
    "KnowledgeCategory",
    "DrugInfo",
    "ClinicalGuide",
]
