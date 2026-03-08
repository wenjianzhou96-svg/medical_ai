"""
医疗智能体系统 - 用户模型

包含用户、角色、权限等数据模型
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.core.database import Base

# 用户角色关联表
user_roles = Table(
    'user_roles',
    Base.metadata,
    Column('user_role_id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False),
    Column('role_id', Integer, ForeignKey('roles.role_id', ondelete='CASCADE'), nullable=False),
    Column('created_at', DateTime, default=datetime.utcnow, nullable=False)
)

# 角色权限关联表
role_permissions = Table(
    'role_permissions',
    Base.metadata,
    Column('role_permission_id', Integer, primary_key=True, autoincrement=True),
    Column('role_id', Integer, ForeignKey('roles.role_id', ondelete='CASCADE'), nullable=False),
    Column('permission_id', Integer, ForeignKey('permissions.permission_id', ondelete='CASCADE'), nullable=False),
    Column('created_at', DateTime, default=datetime.utcnow, nullable=False)
)


class User(Base):
    """用户模型"""
    __tablename__ = 'users'
    
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True, comment='用户名')
    phone = Column(String(20), unique=True, nullable=True, index=True, comment='手机号')
    email = Column(String(100), unique=True, nullable=True, index=True, comment='邮箱')
    password_hash = Column(String(255), nullable=False, comment='密码哈希')
    avatar_url = Column(String(255), nullable=True, comment='头像URL')
    nickname = Column(String(50), nullable=True, comment='昵称')
    gender = Column(Integer, nullable=True, comment='性别: 0-女, 1-男')
    birthday = Column(DateTime, nullable=True, comment='生日')
    status = Column(Integer, default=1, nullable=False, comment='状态: 0-禁用, 1-启用')
    last_login_at = Column(DateTime, nullable=True, comment='最后登录时间')
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False, comment='更新时间')
    
    # 关联关系
    roles = relationship('Role', secondary=user_roles, back_populates='users')
    health_records = relationship('HealthRecord', back_populates='user', cascade='all, delete-orphan')
    consultations = relationship('ConsultationRecord', back_populates='user', cascade='all, delete-orphan')
    vital_signs = relationship('VitalSign', back_populates='user', cascade='all, delete-orphan')
    medication_records = relationship('MedicationRecord', back_populates='user', cascade='all, delete-orphan')
    vaccination_records = relationship('VaccinationRecord', back_populates='user', cascade='all, delete-orphan')
    examination_records = relationship('ExaminationRecord', back_populates='user', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.username}>'


class Role(Base):
    """角色模型"""
    __tablename__ = 'roles'
    
    role_id = Column(Integer, primary_key=True, autoincrement=True)
    role_name = Column(String(50), unique=True, nullable=False, comment='角色名称')
    description = Column(String(255), nullable=True, comment='角色描述')
    status = Column(Integer, default=1, nullable=False, comment='状态: 0-禁用, 1-启用')
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False, comment='更新时间')
    
    # 关联关系
    users = relationship('User', secondary=user_roles, back_populates='roles')
    permissions = relationship('Permission', secondary=role_permissions, back_populates='roles')
    
    def __repr__(self):
        return f'<Role {self.role_name}>'


class Permission(Base):
    """权限模型"""
    __tablename__ = 'permissions'
    
    permission_id = Column(Integer, primary_key=True, autoincrement=True)
    permission_name = Column(String(100), unique=True, nullable=False, comment='权限名称')
    resource = Column(String(50), nullable=False, comment='资源名称')
    action = Column(String(50), nullable=False, comment='操作类型')
    description = Column(String(255), nullable=True, comment='权限描述')
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, comment='创建时间')
    
    # 关联关系
    roles = relationship('Role', secondary=role_permissions, back_populates='permissions')
    
    def __repr__(self):
        return f'<Permission {self.permission_name}>'


class LoginLog(Base):
    """登录日志模型"""
    __tablename__ = 'login_logs'
    
    login_log_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='SET NULL'), nullable=True, comment='用户ID')
    login_type = Column(String(20), nullable=False, comment='登录类型: password/sms/third_party')
    ip_address = Column(String(50), nullable=True, comment='IP地址')
    user_agent = Column(String(255), nullable=True, comment='用户代理')
    device_info = Column(String(255), nullable=True, comment='设备信息')
    login_status = Column(Integer, nullable=False, comment='登录状态: 0-失败, 1-成功')
    failure_reason = Column(String(255), nullable=True, comment='失败原因')
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, comment='创建时间')
    
    # 关联关系
    user = relationship('User', backref='login_logs')
    
    def __repr__(self):
        return f'<LoginLog {self.login_log_id}>'
