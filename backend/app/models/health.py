"""
医疗智能体系统 - 健康管理模型

包含健康档案、体征数据、用药记录、疫苗接种、检查记录等数据模型
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, JSON, DECIMAL
from sqlalchemy.orm import relationship
from app.core.database import Base


class HealthRecord(Base):
    """健康档案模型"""
    __tablename__ = 'health_records'
    
    record_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False, comment='用户ID', unique=True)
    blood_type = Column(String(10), nullable=True, comment='血型')
    height = Column(DECIMAL(5, 2), nullable=True, comment='身高(cm)')
    weight = Column(DECIMAL(5, 2), nullable=True, comment='体重(kg)')
    bmi = Column(DECIMAL(5, 2), nullable=True, comment='BMI指数')
    medical_history = Column(Text, nullable=True, comment='既往病史')
    family_history = Column(Text, nullable=True, comment='家族病史')
    allergy_history = Column(Text, nullable=True, comment='过敏史')
    surgery_history = Column(Text, nullable=True, comment='手术史')
    lifestyle = Column(JSON, nullable=True, comment='生活习惯: 饮食、运动、睡眠等')
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False, comment='更新时间')
    
    # 关联关系
    user = relationship('User', back_populates='health_records')
    
    def __repr__(self):
        return f'<HealthRecord {self.record_id}>'


class VitalSign(Base):
    """体征数据模型"""
    __tablename__ = 'vital_signs'
    
    sign_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False, comment='用户ID')
    sign_type = Column(String(50), nullable=False, comment='体征类型: blood_pressure/heart_rate/temperature/blood_sugar/oxygen/weight')
    value = Column(DECIMAL(10, 2), nullable=False, comment='数值')
    value_ext = Column(DECIMAL(10, 2), nullable=True, comment='扩展值(用于血压等双值)')
    unit = Column(String(20), nullable=False, comment='单位')
    measured_at = Column(DateTime, nullable=False, comment='测量时间')
    source = Column(String(50), nullable=True, comment='数据来源: manual/device/api')
    notes = Column(String(255), nullable=True, comment='备注')
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, comment='创建时间')
    
    # 关联关系
    user = relationship('User', back_populates='vital_signs')
    
    def __repr__(self):
        return f'<VitalSign {self.sign_id}>'


class MedicationRecord(Base):
    """用药记录模型"""
    __tablename__ = 'medication_records'
    
    medication_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False, comment='用户ID')
    medication_name = Column(String(100), nullable=False, comment='药品名称')
    drug_spec = Column(String(100), nullable=True, comment='药品规格')
    dosage = Column(String(50), nullable=False, comment='用法用量')
    frequency = Column(String(50), nullable=False, comment='用药频率')
    route = Column(String(50), nullable=True, comment='用药途径: 口服/注射/外用等')
    start_date = Column(DateTime, nullable=False, comment='开始日期')
    end_date = Column(DateTime, nullable=True, comment='结束日期')
    reminder_enabled = Column(Integer, default=1, nullable=False, comment='是否启用提醒: 0-否, 1-是')
    reminder_times = Column(JSON, nullable=True, comment='提醒时间( JSON数组)')
    indication = Column(String(255), nullable=True, comment='适应症/用药原因')
    side_effects = Column(Text, nullable=True, comment='副作用')
    notes = Column(String(255), nullable=True, comment='备注')
    prescription_id = Column(Integer, nullable=True, comment='关联处方ID')
    doctor_id = Column(Integer, nullable=True, comment='开方医生ID')
    status = Column(Integer, default=1, nullable=False, comment='状态: 0-已停用, 1-使用中')
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False, comment='更新时间')
    
    # 关联关系
    user = relationship('User', back_populates='medication_records')
    
    def __repr__(self):
        return f'<MedicationRecord {self.medication_id}>'


class VaccinationRecord(Base):
    """疫苗接种记录模型"""
    __tablename__ = 'vaccination_records'
    
    vaccination_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False, comment='用户ID')
    vaccine_name = Column(String(100), nullable=False, comment='疫苗名称')
    vaccine_type = Column(String(50), nullable=True, comment='疫苗类型')
    manufacturer = Column(String(100), nullable=True, comment='生产厂家')
    batch_number = Column(String(50), nullable=True, comment='批号')
    dose_number = Column(Integer, nullable=True, comment='接种剂次')
    total_doses = Column(Integer, nullable=True, comment='总剂次')
    vaccination_date = Column(DateTime, nullable=False, comment='接种日期')
    vaccination_agency = Column(String(100), nullable=True, comment='接种机构')
    inoculation_site = Column(String(100), nullable=True, comment='接种部位')
    next_vaccination_date = Column(DateTime, nullable=True, comment='下次接种日期')
    certificate_url = Column(String(255), nullable=True, comment='接种证明URL')
    notes = Column(String(255), nullable=True, comment='备注')
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False, comment='更新时间')
    
    # 关联关系
    user = relationship('User', back_populates='vaccination_records')
    
    def __repr__(self):
        return f'<VaccinationRecord {self.vaccination_id}>'


class ExaminationRecord(Base):
    """检查记录模型"""
    __tablename__ = 'examination_records'
    
    examination_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False, comment='用户ID')
    examination_type = Column(String(50), nullable=False, comment='检查类型: blood_routine/urine_routine/biochemistry/CT/MRI等')
    examination_name = Column(String(100), nullable=True, comment='检查项目名称')
    examination_data = Column(JSON, nullable=True, comment='检查数据')
    examination_date = Column(DateTime, nullable=False, comment='检查日期')
    hospital_name = Column(String(100), nullable=True, comment='医院名称')
    department = Column(String(50), nullable=True, comment='科室')
    doctor_name = Column(String(50), nullable=True, comment='医生姓名')
    report_url = Column(String(255), nullable=True, comment='报告URL')
    summary = Column(Text, nullable=True, comment='检查摘要')
    findings = Column(Text, nullable=True, comment='检查发现')
    conclusions = Column(Text, nullable=True, comment='结论')
    notes = Column(String(255), nullable=True, comment='备注')
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False, comment='更新时间')
    
    # 关联关系
    user = relationship('User', back_populates='examination_records')
    
    def __repr__(self):
        return f'<ExaminationRecord {self.examination_id}>'
