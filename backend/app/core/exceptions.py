"""
医疗智能体系统 - 异常处理模块

提供自定义异常类和全局异常处理器
"""

from typing import Optional, Any, Dict
from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from app.core.logging import logger


class BaseAPIException(HTTPException):
    """基础API异常类"""
    
    def __init__(
        self,
        status_code: int,
        message: str,
        error_code: Optional[str] = None,
        details: Optional[Any] = None
    ):
        super().__init__(status_code=status_code, detail=message)
        self.message = message
        self.error_code = error_code or f"ERR_{status_code}"
        self.details = details


class NotFoundException(BaseAPIException):
    """资源不存在异常"""
    
    def __init__(self, resource: str, resource_id: Optional[int] = None):
        message = f"{resource}不存在"
        if resource_id:
            message = f"{resource}(ID: {resource_id})不存在"
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            message=message,
            error_code="NOT_FOUND"
        )


class UnauthorizedException(BaseAPIException):
    """未授权异常"""
    
    def __init__(self, message: str = "未授权，请先登录"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message=message,
            error_code="UNAUTHORIZED"
        )


class ForbiddenException(BaseAPIException):
    """禁止访问异常"""
    
    def __init__(self, message: str = "权限不足，无法访问"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            message=message,
            error_code="FORBIDDEN"
        )


class BadRequestException(BaseAPIException):
    """请求参数错误异常"""
    
    def __init__(self, message: str, details: Optional[Any] = None):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=message,
            error_code="BAD_REQUEST",
            details=details
        )


class ValidationException(BaseAPIException):
    """数据验证错误异常"""
    
    def __init__(self, message: str, details: Optional[Any] = None):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            message=message,
            error_code="VALIDATION_ERROR",
            details=details
        )


class ConflictException(BaseAPIException):
    """资源冲突异常"""
    
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            message=message,
            error_code="CONFLICT"
        )


class InternalServerException(BaseAPIException):
    """服务器内部错误异常"""
    
    def __init__(self, message: str = "服务器内部错误"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=message,
            error_code="INTERNAL_SERVER_ERROR"
        )


class ServiceUnavailableException(BaseAPIException):
    """服务不可用异常"""
    
    def __init__(self, message: str = "服务暂时不可用"):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            message=message,
            error_code="SERVICE_UNAVAILABLE"
        )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """HTTP异常处理器"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": exc.status_code,
            "message": exc.detail,
            "error_code": getattr(exc, "error_code", None),
            "timestamp": None
        }
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """请求体验证异常处理器"""
    errors = []
    for error in exc.errors():
        errors.append({
            "field": ".".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "code": 422,
            "message": "请求参数验证失败",
            "errors": errors,
            "timestamp": None
        }
    )


async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
    """SQLAlchemy异常处理器"""
    logger.error(f"Database error: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code": 500,
            "message": "数据库操作失败",
            "error_code": "DATABASE_ERROR",
            "timestamp": None
        }
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """通用异常处理器"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code": 500,
            "message": "服务器内部错误",
            "error_code": "INTERNAL_SERVER_ERROR",
            "timestamp": None
        }
    )


def register_exception_handlers(app):
    """注册异常处理器"""
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)
