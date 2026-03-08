"""
医疗智能体系统 - 医生模型

包含医生、排班等数据模型
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Doctor(Base):
    """医生模型"""
    __tablename__ = 'doctors'
    
    doctor_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='SET NULL'), nullable=True, comment='关联用户ID')
    name = Column(String(50), nullable=False, comment='姓名')
    gender = Column(Integer, nullable=True, comment='性别: 0-女, 1-男')
    age = Column(Integer, nullable=True, comment='年龄')
    department = Column(String(50), nullable=False, comment='科室')
    title = Column(String(50), nullable=True, comment='职称')
    specialties = Column(Text, nullable=True, comment='擅长领域')
    certificate_url = Column(String(255), nullable=True, comment='资质证书URL')
    avatar_url = Column(String(255), nullable=True, comment='头像URL')
    introduction = Column(Text, nullable=True, comment='简介')
    phone = Column(String(20), nullable=True, comment='联系电话')
    email = Column(String(100), nullable=True, comment='邮箱')
    status = Column(Integer, default=1, nullable=False, comment='状态: 0-禁用, 1-启用')
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False, comment='更新时间')
    
    # 关联关系
    user = relationship('User', backref='doctor_profile')
    schedules = relationship('Schedule', back_populates='doctor', cascade='all, delete-orphan')
    articles = relationship('Article', back_populates='doctor', cascade='all, delete-orphan')
    consultations = relationship('ConsultationRecord', back_populates='doctor', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Doctor {self.name}>'


class Schedule(Base):
    """医生排班模型"""
    __tablename__ = 'schedules'
    
    schedule_id = Column(Integer, primary_key=True, autoincrement=True)
    doctor_id = Column(Integer, ForeignKey('doctors.doctor_id', ondelete='CASCADE'), nullable=False, comment='医生ID')
    date = Column(DateTime, nullable=False, comment='日期')
    start_time = Column(String(10), nullable=False, comment='开始时间')
    end_time = Column(String(10), nullable=False, comment='结束时间')
    time_slot = Column(String(50), nullable=True, comment='时段: 上午/下午/晚上')
    max_appointments = Column(Integer, default=20, nullable=False, comment='最大预约数')
    current_appointments = Column(Integer, default=0, nullable=False, comment='当前预约数')
    status = Column(Integer, default=1, nullable=False, comment='状态: 0-已取消, 1-正常')
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False, comment='更新时间')
    
    # 关联关系
    doctor = relationship('Doctor', back_populates='schedules')
    
    def __repr__(self):
        return f'<Schedule {self.doctor_id} - {self.date}>'
