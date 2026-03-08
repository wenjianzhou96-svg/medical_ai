"""
医疗智能体系统 - 健康管理路由
"""

from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
from app.core.database import get_db
from app.models.user import User
from app.models.health import VitalSign, HealthRecord
from app.api.v1.deps import get_current_user

router = APIRouter()


class VitalSignCreate(BaseModel):
    """体征数据录入"""
    sign_type: str
    value: float
    value_ext: float | None = None
    unit: str
    measured_at: datetime


class VitalSignResponse(BaseModel):
    """体征数据响应"""
    sign_id: int
    user_id: int
    sign_type: str
    value: float
    unit: str
    measured_at: datetime

    class Config:
        from_attributes = True


@router.post("/vital-signs", response_model=VitalSignResponse, summary="录入体征数据")
async def create_vital_sign(
    request: VitalSignCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """录入体征数据"""
    vital_sign = VitalSign(
        user_id=current_user.user_id,
        sign_type=request.sign_type,
        value=request.value,
        value_ext=request.value_ext,
        unit=request.unit,
        measured_at=request.measured_at
    )
    db.add(vital_sign)
    db.commit()
    db.refresh(vital_sign)
    return VitalSignResponse.model_validate(vital_sign)


@router.get("/vital-signs", response_model=List[VitalSignResponse], summary="获取体征数据列表")
async def get_vital_signs(
    sign_type: str | None = None,
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取体征数据列表"""
    query = db.query(VitalSign).filter(VitalSign.user_id == current_user.user_id)
    if sign_type:
        query = query.filter(VitalSign.sign_type == sign_type)
    vital_signs = query.order_by(VitalSign.measured_at.desc()).offset(skip).limit(limit).all()
    return [VitalSignResponse.model_validate(v) for v in vital_signs]


class HealthRecordResponse(BaseModel):
    """健康档案响应"""
    record_id: int
    user_id: int
    blood_type: str | None = None
    height: float | None = None
    weight: float | None = None

    class Config:
        from_attributes = True


@router.get("/records", response_model=HealthRecordResponse, summary="获取健康档案")
async def get_health_record(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取健康档案"""
    record = db.query(HealthRecord).filter(HealthRecord.user_id == current_user.user_id).first()
    if not record:
        # 如果没有档案，创建一个空的
        record = HealthRecord(user_id=current_user.user_id)
        db.add(record)
        db.commit()
        db.refresh(record)
    return HealthRecordResponse.model_validate(record)
