"""
医疗智能体系统 - 核心模块

提供配置、数据库、安全、日志等核心功能
"""

from app.core.config import settings, get_settings
from app.core.database import get_db, init_db, Base, engine, SessionLocal
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    decode_token,
    verify_token
)
from app.core.logging import logger, setup_logging
from app.core.redis import cache, session_cache, RedisCache, get_redis_client
from app.core.exceptions import (
    BaseAPIException,
    NotFoundException,
    UnauthorizedException,
    ForbiddenException,
    BadRequestException,
    ValidationException,
    ConflictException,
    InternalServerException,
    ServiceUnavailableException,
    register_exception_handlers
)

__all__ = [
    # 配置
    "settings",
    "get_settings",
    # 数据库
    "get_db",
    "init_db",
    "Base",
    "engine",
    "SessionLocal",
    # 安全
    "verify_password",
    "get_password_hash",
    "create_access_token",
    "create_refresh_token",
    "decode_token",
    "verify_token",
    # 日志
    "logger",
    "setup_logging",
    # Redis
    "cache",
    "session_cache",
    "RedisCache",
    "get_redis_client",
    # 异常
    "BaseAPIException",
    "NotFoundException",
    "UnauthorizedException",
    "ForbiddenException",
    "BadRequestException",
    "ValidationException",
    "ConflictException",
    "InternalServerException",
    "ServiceUnavailableException",
    "register_exception_handlers",
]
