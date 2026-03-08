"""
医疗智能体系统 - 问诊路由

提供问诊创建、消息发送、报告生成、医生审核等功能
"""

from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from datetime import datetime

from app.core.database import get_db
from app.models.user import User
from app.models.consultation import ConsultationRecord, ConsultationMessage, AIReport
from app.api.v1.deps import get_current_user
from app.services.consultation import ConsultationService
from app.crud.consultation import ConsultationCRUD, AIReportCRUD

router = APIRouter()


# ==================== 请求模型 ====================

class ConsultationCreate(BaseModel):
    """创建问诊请求"""
    title: Optional[str] = None
    symptoms: str


class MessageSend(BaseModel):
    """发送消息请求"""
    message: str = Field(..., description="消息内容")


class MessageResponse(BaseModel):
    """消息响应"""
    message_id: int
    consultation_id: int
    sender_type: str
    sender_id: Optional[int] = None
    content: str
    created_at: datetime

    class Config:
        from_attributes = True


class ChatResponse(BaseModel):
    """对话响应"""
    reply: str
    suggestion: Optional[str] = None
    is_emergency: bool = False
    follow_up_questions: List[str] = []
    messages: List[MessageResponse] = []


class ReportGenerate(BaseModel):
    """生成报告请求"""
    report_type: str = Field(default="text", description="报告类型: text/image/pdf")


class ReportResponse(BaseModel):
    """报告响应"""
    report_id: int
    consultation_id: int
    user_id: int
    report_type: str
    report_content: Optional[Dict[str, Any]] = None
    report_file_url: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class DoctorReview(BaseModel):
    """医生审核请求"""
    review_content: str = Field(..., description="审核意见")


class ConsultationResponse(BaseModel):
    """问诊响应"""
    consultation_id: int
    user_id: int
    doctor_id: Optional[int] = None
    title: Optional[str] = None
    symptoms: Optional[str] = None
    conversation_history: Optional[List[Dict]] = None
    ai_suggestion: Optional[str] = None
    doctor_review: Optional[str] = None
    severity_level: Optional[int] = None
    status: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ConsultationListResponse(BaseModel):
    """问诊列表响应"""
    items: List[ConsultationResponse]
    total: int
    page: int
    page_size: int


class SeverityResponse(BaseModel):
    """严重程度响应"""
    level: int
    label: str
    description: str
    is_emergency: bool


class StatisticsResponse(BaseModel):
    """问诊统计响应"""
    total: int
    completed: int
    in_progress: int
    pending_review: int
    cancelled: int
    emergency_count: int
    average_severity: float


# ==================== 辅助函数 ====================

def get_severity_info(level: Optional[int]) -> Dict[str, Any]:
    """获取严重程度信息"""
    severity_map = {
        0: {"label": "低危", "description": "症状较轻，可自行处理", "is_emergency": False},
        1: {"label": "中危", "description": "需要关注，建议就医", "is_emergency": False},
        2: {"label": "高危", "description": "建议尽快就医", "is_emergency": False},
        3: {"label": "紧急", "description": "需要立即就医", "is_emergency": True},
    }
    return severity_map.get(level, {"label": "未知", "description": "", "is_emergency": False})


# ==================== 用户API ====================

@router.post("", response_model=ConsultationResponse, summary="创建问诊")
async def create_consultation(
    request: ConsultationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建新的问诊会话，AI会自动回复"""
    service = ConsultationService(db)
    consultation = await service.create_consultation(
        user_id=current_user.user_id,
        title=request.title,
        symptoms=request.symptoms
    )
    return ConsultationResponse.model_validate(consultation)


@router.get("", response_model=ConsultationListResponse, summary="获取问诊列表")
async def get_consultations(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    status: Optional[int] = Query(None, description="问诊状态筛选"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取当前用户的问诊列表"""
    skip = (page - 1) * page_size
    service = ConsultationService(db)
    consultations, total = service.get_user_consultations(
        user_id=current_user.user_id,
        skip=skip,
        limit=page_size,
        status=status
    )
    return ConsultationListResponse(
        items=[ConsultationResponse.model_validate(c) for c in consultations],
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/", response_model=ConsultationListResponse, summary="获取问诊列表(带斜杠)")
async def get_consultations_with_slash(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    status: Optional[int] = Query(None, description="问诊状态筛选"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取当前用户的问诊列表(带尾部斜杠)"""
    return await get_consultations(page, page_size, status, current_user, db)


@router.get("/{consultation_id}", response_model=ConsultationResponse, summary="获取问诊详情")
async def get_consultation(
    consultation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取问诊详情（包括对话历史）"""
    service = ConsultationService(db)
    consultation = service.get_consultation(consultation_id)
    
    # 检查权限
    if consultation.user_id != current_user.user_id:
        from app.core.exceptions import ForbiddenException
        raise ForbiddenException("无权查看此问诊记录")
    
    return ConsultationResponse.model_validate(consultation)


@router.delete("/{consultation_id}", status_code=204, summary="删除问诊")
async def delete_consultation(
    consultation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """删除问诊记录（物理删除）"""
    service = ConsultationService(db)
    
    # 检查问诊是否存在
    consultation = service.get_consultation(consultation_id)
    if not consultation:
        from app.core.exceptions import NotFoundException
        raise NotFoundException("问诊记录", consultation_id)
    
    # 检查权限（只有创建者可以删除）
    if consultation.user_id != current_user.user_id:
        from app.core.exceptions import ForbiddenException
        raise ForbiddenException("无权删除此问诊记录")
    
    # 检查状态（进行中的问诊不能删除）
    if consultation.status == 0:
        from app.core.exceptions import BadRequestException
        raise BadRequestException("进行中的问诊不能删除，请先取消或完成问诊")
    
    # 执行删除
    service.delete_consultation(consultation_id)


@router.post("/{consultation_id}/messages", response_model=ChatResponse, summary="发送消息")
async def send_message(
    consultation_id: int,
    request: MessageSend,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """发送问诊消息，AI会自动回复"""
    service = ConsultationService(db)
    
    # 获取用户健康信息
    user_info = None
    # TODO: 从健康档案获取用户健康信息
    
    result = await service.send_message(
        consultation_id=consultation_id,
        user_id=current_user.user_id,
        message=request.message,
        user_info=user_info
    )
    
    # 获取更新后的消息列表
    crud = ConsultationCRUD()
    messages = crud.get_messages(db, consultation_id)
    
    return ChatResponse(
        reply=result["reply"],
        suggestion=result.get("suggestion"),
        is_emergency=result.get("is_emergency", False),
        follow_up_questions=result.get("follow_up_questions", []),
        messages=[MessageResponse.model_validate(m) for m in messages]
    )


@router.get("/{consultation_id}/messages", response_model=List[MessageResponse], summary="获取消息列表")
async def get_messages(
    consultation_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取问诊的消息列表"""
    # 检查权限
    consultation = db.query(ConsultationRecord).filter(
        ConsultationRecord.consultation_id == consultation_id
    ).first()
    
    if not consultation:
        from app.core.exceptions import NotFoundException
        raise NotFoundException("问诊记录", consultation_id)
    
    if consultation.user_id != current_user.user_id:
        from app.core.exceptions import ForbiddenException
        raise ForbiddenException("无权查看此问诊记录")
    
    crud = ConsultationCRUD()
    messages = crud.get_messages(db, consultation_id, skip, limit)
    return [MessageResponse.model_validate(m) for m in messages]


@router.post("/{consultation_id}/finish", response_model=ConsultationResponse, summary="完成问诊")
async def finish_consultation(
    consultation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """完成问诊，生成诊断建议（自动进入待审核状态）"""
    service = ConsultationService(db)
    
    # 获取用户健康信息
    user_info = None
    # TODO: 从健康档案获取用户健康信息
    
    consultation = await service.finish_consultation(
        consultation_id=consultation_id,
        user_id=current_user.user_id,
        user_info=user_info
    )
    
    # 检查权限
    if consultation.user_id != current_user.user_id:
        from app.core.exceptions import ForbiddenException
        raise ForbiddenException("无权操作此问诊记录")
    
    return ConsultationResponse.model_validate(consultation)


@router.post("/{consultation_id}/report", response_model=ReportResponse, summary="生成报告")
async def generate_report(
    consultation_id: int,
    request: ReportGenerate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """生成问诊报告"""
    service = ConsultationService(db)
    
    # 检查权限
    consultation = service.get_consultation(consultation_id)
    if consultation.user_id != current_user.user_id:
        from app.core.exceptions import ForbiddenException
        raise ForbiddenException("无权操作此问诊记录")
    
    report_content = await service.generate_report(
        consultation_id=consultation_id,
        user_id=current_user.user_id
    )
    
    # 获取生成的报告
    report_crud = AIReportCRUD()
    reports = report_crud.get_by_consultation(db, consultation_id)
    report = reports[0] if reports else None
    
    if not report:
        from app.core.exceptions import InternalServerException
        raise InternalServerException("报告生成失败")
    
    return ReportResponse.model_validate(report)


@router.get("/{consultation_id}/reports", response_model=List[ReportResponse], summary="获取报告列表")
async def get_reports(
    consultation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取问诊的报告列表"""
    # 检查权限
    consultation = db.query(ConsultationRecord).filter(
        ConsultationRecord.consultation_id == consultation_id
    ).first()
    
    if not consultation:
        from app.core.exceptions import NotFoundException
        raise NotFoundException("问诊记录", consultation_id)
    
    if consultation.user_id != current_user.user_id:
        from app.core.exceptions import ForbiddenException
        raise ForbiddenException("无权查看此问诊记录")
    
    report_crud = AIReportCRUD()
    reports = report_crud.get_by_consultation(db, consultation_id)
    return [ReportResponse.model_validate(r) for r in reports]


@router.get("/{consultation_id}/severity", response_model=SeverityResponse, summary="获取严重程度")
async def get_severity(
    consultation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取问诊的严重程度评估"""
    # 检查权限
    consultation = db.query(ConsultationRecord).filter(
        ConsultationRecord.consultation_id == consultation_id
    ).first()
    
    if not consultation:
        from app.core.exceptions import NotFoundException
        raise NotFoundException("问诊记录", consultation_id)
    
    if consultation.user_id != current_user.user_id:
        from app.core.exceptions import ForbiddenException
        raise ForbiddenException("无权查看此问诊记录")
    
    severity_info = get_severity_info(consultation.severity_level)
    return SeverityResponse(
        level=consultation.severity_level or 0,
        label=severity_info["label"],
        description=severity_info["description"],
        is_emergency=severity_info["is_emergency"]
    )


@router.post("/{consultation_id}/cancel", response_model=ConsultationResponse, summary="取消问诊")
async def cancel_consultation(
    consultation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """取消问诊"""
    service = ConsultationService(db)
    
    # 检查权限
    consultation = service.get_consultation(consultation_id)
    if consultation.user_id != current_user.user_id:
        from app.core.exceptions import ForbiddenException
        raise ForbiddenException("无权操作此问诊记录")
    
    consultation = service.cancel_consultation(consultation_id)
    return ConsultationResponse.model_validate(consultation)


# ==================== 管理后台API ====================

@router.get("/admin/list", response_model=ConsultationListResponse, summary="获取所有问诊列表（管理）")
async def get_admin_consultations(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    status: Optional[int] = Query(None, description="问诊状态筛选"),
    severity_level: Optional[int] = Query(None, description="严重程度筛选"),
    user_id: Optional[int] = Query(None, description="用户ID筛选"),
    doctor_id: Optional[int] = Query(None, description="医生ID筛选"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取所有问诊列表（管理员/医生用）"""
    # 检查权限（需要医生或管理员角色）
    from app.api.v1.deps import check_permissions
    await check_permissions(["consultation:list"])
    
    skip = (page - 1) * page_size
    service = ConsultationService(db)
    consultations, total = service.get_all_consultations(
        skip=skip,
        limit=page_size,
        user_id=user_id,
        doctor_id=doctor_id,
        status=status,
        severity_level=severity_level
    )
    return ConsultationListResponse(
        items=[ConsultationResponse.model_validate(c) for c in consultations],
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/admin/{consultation_id}", response_model=ConsultationResponse, summary="获取问诊详情（管理）")
async def get_admin_consultation(
    consultation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取问诊详情（管理员/医生用）"""
    # 检查权限
    from app.api.v1.deps import check_permissions
    await check_permissions(["consultation:list"])
    
    service = ConsultationService(db)
    consultation = service.get_consultation(consultation_id)
    return ConsultationResponse.model_validate(consultation)


@router.post("/admin/{consultation_id}/review", response_model=ConsultationResponse, summary="医生审核")
async def doctor_review(
    consultation_id: int,
    request: DoctorReview,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """医生审核AI诊断建议"""
    # 检查权限（需要医生角色）
    from app.api.v1.deps import check_permissions
    await check_permissions(["consultation:review"])
    
    service = ConsultationService(db)
    
    # TODO: 从医生表获取当前用户的医生ID
    doctor_id = current_user.user_id  # 临时使用用户ID
    
    consultation = service.doctor_review(
        consultation_id=consultation_id,
        doctor_id=doctor_id,
        review_content=request.review_content
    )
    return ConsultationResponse.model_validate(consultation)


@router.get("/admin/statistics", response_model=StatisticsResponse, summary="问诊统计")
async def get_statistics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取问诊统计数据"""
    # 检查权限
    from app.api.v1.deps import check_permissions
    await check_permissions(["consultation:list"])
    
    # 查询统计数据
    from sqlalchemy import func
    
    total = db.query(func.count(ConsultationRecord.consultation_id)).scalar() or 0
    completed = db.query(func.count(ConsultationRecord.consultation_id)).filter(
        ConsultationRecord.status == 1
    ).scalar() or 0
    in_progress = db.query(func.count(ConsultationRecord.consultation_id)).filter(
        ConsultationRecord.status == 0
    ).scalar() or 0
    pending_review = db.query(func.count(ConsultationRecord.consultation_id)).filter(
        ConsultationRecord.status == 3
    ).scalar() or 0
    cancelled = db.query(func.count(ConsultationRecord.consultation_id)).filter(
        ConsultationRecord.status == 2
    ).scalar() or 0
    emergency_count = db.query(func.count(ConsultationRecord.consultation_id)).filter(
        ConsultationRecord.severity_level == 3
    ).scalar() or 0
    
    # 计算平均严重程度
    avg_severity = db.query(func.avg(ConsultationRecord.severity_level)).filter(
        ConsultationRecord.severity_level.isnot(None)
    ).scalar() or 0
    
    return StatisticsResponse(
        total=total,
        completed=completed,
        in_progress=in_progress,
        pending_review=pending_review,
        cancelled=cancelled,
        emergency_count=emergency_count,
        average_severity=float(avg_severity)
    )
