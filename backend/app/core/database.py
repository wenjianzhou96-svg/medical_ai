"""
医疗智能体系统 - 数据库连接模块

提供SQLAlchemy数据库连接、Session管理等功能
"""

from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings

# 创建数据库引擎
engine = create_engine(
    settings.database_url,
    echo=settings.database_echo,
    pool_size=settings.db_pool_size,
    max_overflow=settings.db_max_overflow,
    pool_pre_ping=True,
    pool_recycle=3600,
)

# 创建会话工厂
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# 创建基类
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    获取数据库会话
    
    用于FastAPI的依赖注入
    
    Yields:
        Session: 数据库会话对象
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """初始化数据库，创建所有表"""
    Base.metadata.create_all(bind=engine)
