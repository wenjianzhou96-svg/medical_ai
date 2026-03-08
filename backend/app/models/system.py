"""
医疗智能体系统 - 系统管理模型

包含系统配置、操作日志、通知等数据模型
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base


class SystemConfig(Base):
    """系统配置模型"""
    __tablename__ = 'system_configs'
    
    config_id = Column(Integer, primary_key=True, autoincrement=True)
    config_key = Column(String(100), unique=True, nullable=False, comment='配置键')
    config_value = Column(Text, nullable=True, comment='配置值')
    config_type = Column(String(50), nullable=False, comment='配置类型: string/integer/boolean/json')
    description = Column(String(255), nullable=True, comment='配置描述')
    is_system = Column(Integer, default=0, nullable=False, comment='是否系统配置: 0-否, 1-是')
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False, comment='更新时间')
    
    def __repr__(self):
        return f'<SystemConfig {self.config_key}>'


class OperationLog(Base):
    """操作日志模型"""
    __tablename__ = 'operation_logs'
    
    log_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='SET NULL'), nullable=True, comment='用户ID')
    username = Column(String(50), nullable=True, comment='用户名')
    operation_type = Column(String(50), nullable=False, comment='操作类型')
    resource_type = Column(String(50), nullable=False, comment='资源类型')
    resource_id = Column(Integer, nullable=True, comment='资源ID')
    operation_desc = Column(String(255), nullable=True, comment='操作描述')
    request_method = Column(String(10), nullable=True, comment='请求方法')
    request_path = Column(String(255), nullable=True, comment='请求路径')
    request_params = Column(JSON, nullable=True, comment='请求参数')
    request_ip = Column(String(50), nullable=True, comment='请求IP')
    user_agent = Column(String(255), nullable=True, comment='用户代理')
    response_status = Column(Integer, nullable=True, comment='响应状态')
    error_message = Column(Text, nullable=True, comment='错误信息')
    duration = Column(Integer, nullable=True, comment='请求耗时(毫秒)')
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, comment='创建时间')
    
    # 关联关系
    user = relationship('User', backref='operation_logs')
    
    def __repr__(self):
        return f'<OperationLog {self.log_id}>'


class Notification(Base):
    """通知消息模型"""
    __tablename__ = 'notifications'
    
    notification_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False, comment='用户ID')
    notification_type = Column(String(50), nullable=False, comment='通知类型: system/consultation/reminder/article')
    title = Column(String(200), nullable=False, comment='通知标题')
    content = Column(Text, nullable=False, comment='通知内容')
    link_url = Column(String(255), nullable=True, comment='链接URL')
    is_read = Column(Integer, default=0, nullable=False, comment='是否已读: 0-未读, 1-已读')
    read_at = Column(DateTime, nullable=True, comment='阅读时间')
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, comment='创建时间')
    
    # 关联关系
    user = relationship('User', backref='notifications')
    
    def __repr__(self):
        return f'<Notification {self.notification_id}>'


class AlertRecord(Base):
    """告警记录模型"""
    __tablename__ = 'alert_records'
    
    alert_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=True, comment='用户ID')
    consultation_id = Column(Integer, ForeignKey('consultation_records.consultation_id', ondelete='SET NULL'), nullable=True, comment='关联问诊ID')
    alert_type = Column(String(50), nullable=False, comment='告警类型: emergency/severity/reminder')
    severity = Column(Integer, nullable=False, comment='严重程度: 0-低, 1-中, 2-高, 3-紧急')
    title = Column(String(200), nullable=False, comment='告警标题')
    content = Column(Text, nullable=False, comment='告警内容')
    symptoms = Column(Text, nullable=True, comment='相关症状')
    suggested_action = Column(Text, nullable=True, comment='建议措施')
    contact_notified = Column(JSON, nullable=True, comment='已通知联系人')
    status = Column(Integer, default=0, nullable=False, comment='状态: 0-待处理, 1-处理中, 2-已解决, 3-已忽略')
    resolved_at = Column(DateTime, nullable=True, comment='处理时间')
    resolved_by = Column(Integer, ForeignKey('users.user_id', ondelete='SET NULL'), nullable=True, comment='处理人ID')
    resolution_notes = Column(Text, nullable=True, comment='处理备注')
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, comment='创建时间')
    
    # 关联关系
    user = relationship('User', foreign_keys=[user_id], backref='alerts')
    consultation = relationship('ConsultationRecord', backref='alerts')
    resolver = relationship('User', foreign_keys=[resolved_by])
    
    def __repr__(self):
        return f'<AlertRecord {self.alert_id}>'


class FollowUpPlan(Base):
    """随访计划模型"""
    __tablename__ = 'follow_up_plans'
    
    plan_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False, comment='用户ID')
    doctor_id = Column(Integer, ForeignKey('doctors.doctor_id', ondelete='SET NULL'), nullable=True, comment='医生ID')
    consultation_id = Column(Integer, ForeignKey('consultation_records.consultation_id', ondelete='SET NULL'), nullable=True, comment='关联问诊ID')
    plan_type = Column(String(50), nullable=False, comment='计划类型: periodic/disease/medication')
    title = Column(String(200), nullable=False, comment='计划标题')
    description = Column(Text, nullable=True, comment='计划描述')
    frequency = Column(String(50), nullable=True, comment='随访频率')
    start_date = Column(DateTime, nullable=False, comment='开始日期')
    end_date = Column(DateTime, nullable=True, comment='结束日期')
    reminder_enabled = Column(Integer, default=1, nullable=False, comment='是否启用提醒: 0-否, 1-是')
    reminder_times = Column(JSON, nullable=True, comment='提醒时间')
    content_template = Column(Text, nullable=True, comment='随访内容模板')
    status = Column(Integer, default=1, nullable=False, comment='状态: 0-已暂停, 1-进行中, 2-已完成')
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False, comment='更新时间')
    
    # 关联关系
    user = relationship('User', foreign_keys=[user_id], backref='follow_up_plans')
    doctor = relationship('Doctor', backref='follow_up_plans')
    consultation = relationship('ConsultationRecord', backref='follow_up_plans')
    
    def __repr__(self):
        return f'<FollowUpPlan {self.plan_id}>'


class FollowUpRecord(Base):
    """随访记录模型"""
    __tablename__ = 'follow_up_records'
    
    record_id = Column(Integer, primary_key=True, autoincrement=True)
    plan_id = Column(Integer, ForeignKey('follow_up_plans.plan_id', ondelete='CASCADE'), nullable=False, comment='计划ID')
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False, comment='用户ID')
    execute_type = Column(String(50), nullable=False, comment='执行类型: manual/ai/phone')
    executor_id = Column(Integer, nullable=True, comment='执行人ID')
    content = Column(Text, nullable=True, comment='随访内容')
    result = Column(JSON, nullable=True, comment='随访结果')
    next_action = Column(Text, nullable=True, comment='后续建议')
    satisfaction = Column(Integer, nullable=True, comment='满意度评分(1-5)')
    executed_at = Column(DateTime, nullable=False, comment='执行时间')
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, comment='创建时间')
    
    # 关联关系
    plan = relationship('FollowUpPlan', backref='records')
    user = relationship('User', backref='follow_up_records')
    
    def __repr__(self):
        return f'<FollowUpRecord {self.record_id}>'
