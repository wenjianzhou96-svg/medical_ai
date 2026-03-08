"""
医疗智能体系统 - 知识库模型

包含医学知识、药品信息等数据模型
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base


class MedicalKnowledge(Base):
    """医学知识模型"""
    __tablename__ = 'medical_knowledge'
    
    knowledge_id = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey('knowledge_categories.category_id', ondelete='SET NULL'), nullable=True, comment='分类ID')
    title = Column(String(200), nullable=False, comment='标题')
    keywords = Column(String(500), nullable=True, comment='关键词')
    content = Column(Text, nullable=False, comment='内容')
    summary = Column(String(500), nullable=True, comment='摘要')
    source = Column(String(100), nullable=True, comment='来源')
    author = Column(String(50), nullable=True, comment='作者')
    tags = Column(String(255), nullable=True, comment='标签')
    view_count = Column(Integer, default=0, nullable=False, comment='浏览量')
    status = Column(Integer, default=0, nullable=False, comment='状态: 0-草稿, 1-待审核, 2-已发布')
    version = Column(Integer, default=1, nullable=False, comment='版本号')
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False, comment='更新时间')
    
    # 关联关系
    category = relationship('KnowledgeCategory', backref='knowledge_items')


class KnowledgeCategory(Base):
    """知识分类模型"""
    __tablename__ = 'knowledge_categories'
    
    category_id = Column(Integer, primary_key=True, autoincrement=True)
    category_name = Column(String(50), nullable=False, comment='分类名称')
    parent_id = Column(Integer, ForeignKey('knowledge_categories.category_id', ondelete='SET NULL'), nullable=True, comment='父分类ID')
    sort_order = Column(Integer, default=0, nullable=False, comment='排序号')
    description = Column(String(255), nullable=True, comment='分类描述')
    icon = Column(String(255), nullable=True, comment='图标')
    status = Column(Integer, default=1, nullable=False, comment='状态: 0-禁用, 1-启用')
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False, comment='更新时间')
    
    # 关联关系
    parent = relationship('KnowledgeCategory', remote_side=[category_id], backref='children')


class DrugInfo(Base):
    """药品信息模型"""
    __tablename__ = 'drug_info'
    
    drug_id = Column(Integer, primary_key=True, autoincrement=True)
    drug_name = Column(String(100), nullable=False, comment='药品名称')
    generic_name = Column(String(100), nullable=True, comment='通用名')
    english_name = Column(String(100), nullable=True, comment='英文名')
    drug_type = Column(String(50), nullable=True, comment='药品类型')
    specification = Column(String(200), nullable=True, comment='规格')
    manufacturer = Column(String(100), nullable=True, comment='生产厂家')
    usage = Column(String(100), nullable=True, comment='用法用量')
    indication = Column(Text, nullable=True, comment='适应症')
    contraindication = Column(Text, nullable=True, comment='禁忌')
    side_effect = Column(Text, nullable=True, comment='不良反应')
    interaction = Column(Text, nullable=True, comment='药物相互作用')
    precautions = Column(Text, nullable=True, comment='注意事项')
    storage = Column(String(255), nullable=True, comment='贮藏方法')
    packaging = Column(String(100), nullable=True, comment='包装规格')
    approval_number = Column(String(100), nullable=True, comment='批准文号')
    status = Column(Integer, default=1, nullable=False, comment='状态: 0-禁用, 1-启用')
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False, comment='更新时间')
    
    def __repr__(self):
        return f'<DrugInfo {self.drug_name}>'


class ClinicalGuide(Base):
    """临床指南模型"""
    __tablename__ = 'clinical_guides'
    
    guide_id = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey('knowledge_categories.category_id', ondelete='SET NULL'), nullable=True, comment='分类ID')
    title = Column(String(200), nullable=False, comment='指南标题')
    guide_code = Column(String(100), nullable=True, comment='指南编号')
    version = Column(String(50), nullable=True, comment='版本')
    source = Column(String(100), nullable=True, comment='来源')
    publish_date = Column(DateTime, nullable=True, comment='发布日期')
    content = Column(Text, nullable=False, comment='指南内容')
    summary = Column(String(500), nullable=True, comment='摘要')
    applicable_scope = Column(String(255), nullable=True, comment='适用范围')
    status = Column(Integer, default=0, nullable=False, comment='状态: 0-草稿, 1-待审核, 2-已发布')
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False, comment='更新时间')
    
    # 关联关系
    category = relationship('KnowledgeCategory', backref='guides')
    
    def __repr__(self):
        return f'<ClinicalGuide {self.title}>'
