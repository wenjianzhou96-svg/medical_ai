"""
医疗智能体系统 - 内容管理模型

包含文章、分类、评论、审核等数据模型
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base


class Category(Base):
    """分类模型"""
    __tablename__ = 'categories'
    
    category_id = Column(Integer, primary_key=True, autoincrement=True)
    category_name = Column(String(50), nullable=False, comment='分类名称')
    parent_id = Column(Integer, ForeignKey('categories.category_id', ondelete='SET NULL'), nullable=True, comment='父分类ID')
    sort_order = Column(Integer, default=0, nullable=False, comment='排序号')
    description = Column(String(255), nullable=True, comment='分类描述')
    icon = Column(String(255), nullable=True, comment='分类图标')
    status = Column(Integer, default=1, nullable=False, comment='状态: 0-禁用, 1-启用')
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False, comment='更新时间')
    
    # 关联关系
    parent = relationship('Category', remote_side=[category_id], backref='children')
    articles = relationship('Article', back_populates='category', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Category {self.category_name}>'


class Article(Base):
    """文章模型"""
    __tablename__ = 'articles'
    
    article_id = Column(Integer, primary_key=True, autoincrement=True)
    doctor_id = Column(Integer, ForeignKey('doctors.doctor_id', ondelete='SET NULL'), nullable=True, comment='医生ID')
    category_id = Column(Integer, ForeignKey('categories.category_id', ondelete='RESTRICT'), nullable=False, comment='分类ID')
    title = Column(String(200), nullable=False, comment='文章标题')
    summary = Column(String(500), nullable=True, comment='文章摘要')
    content = Column(Text, nullable=False, comment='文章内容')
    cover_image = Column(String(255), nullable=True, comment='封面图片URL')
    tags = Column(String(255), nullable=True, comment='标签(逗号分隔)')
    source = Column(String(100), nullable=True, comment='来源')
    view_count = Column(Integer, default=0, nullable=False, comment='阅读量')
    like_count = Column(Integer, default=0, nullable=False, comment='点赞数')
    comment_count = Column(Integer, default=0, nullable=False, comment='评论数')
    share_count = Column(Integer, default=0, nullable=False, comment='分享数')
    status = Column(Integer, default=0, nullable=False, comment='状态: 0-草稿, 1-待审核, 2-已发布, 3-已下架')
    published_at = Column(DateTime, nullable=True, comment='发布时间')
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False, comment='更新时间')
    
    # 关联关系
    doctor = relationship('Doctor', back_populates='articles')
    category = relationship('Category', back_populates='articles')
    comments = relationship('Comment', back_populates='article', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Article {self.title}>'


class Comment(Base):
    """评论模型"""
    __tablename__ = 'comments'
    
    comment_id = Column(Integer, primary_key=True, autoincrement=True)
    article_id = Column(Integer, ForeignKey('articles.article_id', ondelete='CASCADE'), nullable=False, comment='文章ID')
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False, comment='用户ID')
    parent_id = Column(Integer, ForeignKey('comments.comment_id', ondelete='CASCADE'), nullable=True, comment='父评论ID')
    content = Column(Text, nullable=False, comment='评论内容')
    like_count = Column(Integer, default=0, nullable=False, comment='点赞数')
    reply_count = Column(Integer, default=0, nullable=False, comment='回复数')
    status = Column(Integer, default=0, nullable=False, comment='状态: 0-待审核, 1-已通过, 2-已拒绝')
    ip_address = Column(String(50), nullable=True, comment='IP地址')
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False, comment='更新时间')
    
    # 关联关系
    article = relationship('Article', back_populates='comments')
    user = relationship('User', backref='comments')
    parent = relationship('Comment', remote_side=[comment_id], backref='replies')
    
    def __repr__(self):
        return f'<Comment {self.comment_id}>'


class Review(Base):
    """审核模型"""
    __tablename__ = 'reviews'
    
    review_id = Column(Integer, primary_key=True, autoincrement=True)
    reviewable_type = Column(String(50), nullable=False, comment='审核对象类型: article/comment/knowledge')
    reviewable_id = Column(Integer, nullable=False, comment='审核对象ID')
    reviewer_id = Column(Integer, ForeignKey('users.user_id', ondelete='SET NULL'), nullable=True, comment='审核人ID')
    review_result = Column(Integer, default=0, nullable=False, comment='审核结果: 0-待审核, 1-通过, 2-拒绝')
    review_comment = Column(Text, nullable=True, comment='审核意见')
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False, comment='更新时间')
    
    # 关联关系
    reviewer = relationship('User', backref='reviews')
    
    def __repr__(self):
        return f'<Review {self.review_id}>'
