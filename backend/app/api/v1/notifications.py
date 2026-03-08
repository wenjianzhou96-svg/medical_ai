"""
医疗智能体系统 - 通知路由
"""

from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime

from app.core.database import get_db
from app.models.user import User
from app.models.system import Notification
from app.api.v1.deps import get_current_user

router = APIRouter()


class NotificationResponse(BaseModel):
    """通知响应"""
    notification_id: int
    notification_type: str
    title: str
    content: str
    is_read: int
    created_at: datetime

    class Config:
        from_attributes = True


@router.get("", response_model=List[NotificationResponse], summary="获取通知列表")
async def get_notifications(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取通知列表"""
    notifications = db.query(Notification).filter(
        Notification.user_id == current_user.user_id
    ).order_by(Notification.created_at.desc()).offset(skip).limit(limit).all()
    return [NotificationResponse.model_validate(n) for n in notifications]


@router.get("/", response_model=List[NotificationResponse], summary="获取通知列表(带斜杠)")
async def get_notifications_with_slash(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取通知列表(带尾部斜杠)"""
    return await get_notifications(skip, limit, current_user, db)


@router.get("/unread-count", summary="获取未读通知数量")
async def get_unread_count(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取未读通知数量"""
    count = db.query(Notification).filter(
        Notification.user_id == current_user.user_id,
        Notification.is_read == 0
    ).count()
    return {"unread_count": count}


@router.put("/{notification_id}/read", summary="标记通知为已读")
async def mark_as_read(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """标记通知为已读"""
    notification = db.query(Notification).filter(
        Notification.notification_id == notification_id,
        Notification.user_id == current_user.user_id
    ).first()
    if notification:
        notification.is_read = 1
        notification.read_at = datetime.utcnow()
        db.commit()
    return {"message": "操作成功"}
