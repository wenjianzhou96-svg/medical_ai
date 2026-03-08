"""
医疗智能体系统 - 问诊模型

包含问诊记录、问诊消息、AI报告等数据模型
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base


class ConsultationRecord(Base):
    """问诊记录模型"""
    __tablename__ = 'consultation_records'
    
    consultation_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False, comment='用户ID')
    doctor_id = Column(Integer, ForeignKey('doctors.doctor_id', ondelete='SET NULL'), nullable=True, comment='医生ID')
    title = Column(String(200), nullable=True, comment='问诊标题')
    symptoms = Column(Text, nullable=True, comment='症状描述')
    conversation_history = Column(JSON, nullable=True, comment='对话历史')
    ai_suggestion = Column(Text, nullable=True, comment='AI诊断建议')
    doctor_review = Column(Text, nullable=True, comment='医生审核意见')
    severity_level = Column(Integer, nullable=True, comment='严重程度: 0-低, 1-中, 2-高, 3-紧急')
    status = Column(Integer, default=0, nullable=False, comment='状态: 0-进行中, 1-已完成, 2-已取消, 3-待审核')
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False, comment='更新时间')
    
    # 关联关系
    user = relationship('User', back_populates='consultations')
    doctor = relationship('Doctor', back_populates='consultations')
    messages = relationship('ConsultationMessage', back_populates='consultation', cascade='all, delete-orphan')
    reports = relationship('AIReport', back_populates='consultation', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<ConsultationRecord {self.consultation_id}>'


class ConsultationMessage(Base):
    """问诊消息模型"""
    __tablename__ = 'consultation_messages'
    
    message_id = Column(Integer, primary_key=True, autoincrement=True)
    consultation_id = Column(Integer, ForeignKey('consultation_records.consultation_id', ondelete='CASCADE'), nullable=False, comment='问诊ID')
    sender_type = Column(String(20), nullable=False, comment='发送者类型: user/ai/doctor')
    sender_id = Column(Integer, nullable=True, comment='发送者ID')
    content = Column(Text, nullable=False, comment='消息内容')
    message_metadata = Column(JSON, nullable=True, comment='元数据')
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, comment='创建时间')
    
    # 关联关系
    consultation = relationship('ConsultationRecord', back_populates='messages')
    
    def __repr__(self):
        return f'<ConsultationMessage {self.message_id}>'


class AIReport(Base):
    """AI报告模型"""
    __tablename__ = 'ai_reports'
    
    report_id = Column(Integer, primary_key=True, autoincrement=True)
    consultation_id = Column(Integer, ForeignKey('consultation_records.consultation_id', ondelete='CASCADE'), nullable=False, comment='问诊ID')
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False, comment='用户ID')
    report_type = Column(String(20), default='text', nullable=False, comment='报告类型: text/image/pdf')
    report_content = Column(JSON, nullable=True, comment='报告内容')
    report_file_url = Column(String(255), nullable=True, comment='报告文件URL')
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, comment='创建时间')
    
    # 关联关系
    consultation = relationship('ConsultationRecord', back_populates='reports')
    user = relationship('User', backref='ai_reports')
    
    def __repr__(self):
        return f'<AIReport {self.report_id}>'
