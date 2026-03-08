"""
医疗智能体系统 - 医生路由
"""

from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime

from app.core.database import get_db
from app.models.doctor import Doctor

router = APIRouter()


class DoctorResponse(BaseModel):
    """医生响应"""
    doctor_id: int
    name: str
    department: str
    title: str | None = None
    avatar_url: str | None = None
    introduction: str | None = None
    specialties: str | None = None

    class Config:
        from_attributes = True


@router.get("", response_model=List[DoctorResponse], summary="获取医生列表")
async def get_doctors(
    department: str | None = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """获取医生列表"""
    query = db.query(Doctor).filter(Doctor.status == 1)
    if department:
        query = query.filter(Doctor.department == department)
    doctors = query.order_by(Doctor.doctor_id).offset(skip).limit(limit).all()
    return [DoctorResponse.model_validate(d) for d in doctors]


@router.get("/", response_model=List[DoctorResponse], summary="获取医生列表(带斜杠)")
async def get_doctors_with_slash(
    department: str | None = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """获取医生列表(带尾部斜杠)"""
    return await get_doctors(department, skip, limit, db)


@router.get("/{doctor_id}", response_model=DoctorResponse, summary="获取医生详情")
async def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    """获取医生详情"""
    doctor = db.query(Doctor).filter(
        Doctor.doctor_id == doctor_id,
        Doctor.status == 1
    ).first()
    if not doctor:
        from app.core.exceptions import NotFoundException
        raise NotFoundException("医生", doctor_id)
    return DoctorResponse.model_validate(doctor)
