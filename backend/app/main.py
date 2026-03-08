"""
医疗智能体系统 - 主入口文件

基于大语言模型的医疗智能体系统API服务
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from datetime import datetime

from app.core.config import settings
from app.core.database import engine, Base
from app.core.logging import logger, setup_logging
from app.core.exceptions import register_exception_handlers
from app.api.v1 import router as api_v1_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 应用启动时执行
    logger.info(f"正在启动 {settings.app_name} v{settings.app_version}")
    logger.info(f"调试模式: {settings.debug}")
    
    # 创建数据库表
    Base.metadata.create_all(bind=engine)
    logger.info("数据库表创建完成")
    
    # 初始化数据
    # await init_default_data()
    
    logger.info(f"{settings.app_name} 启动完成")
    
    yield
    
    # 应用关闭时执行
    logger.info(f"正在关闭 {settings.app_name}")
    engine.dispose()
    logger.info("数据库连接已关闭")


# 创建FastAPI应用
app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# 注册异常处理器
register_exception_handlers(app)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 请求日志中间件
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """记录请求日志"""
    start_time = datetime.utcnow()
    
    response = await call_next(request)
    
    duration = (datetime.utcnow() - start_time).total_seconds() * 1000
    
    logger.info(
        f"{request.method} {request.url.path} - "
        f"状态码: {response.status_code} - "
        f"耗时: {duration:.2f}ms"
    )
    
    return response


# 根路由
@app.get("/")
async def root():
    """根路径"""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "description": settings.app_description,
        "docs": "/docs",
        "api": "/api/v1"
    }


# 健康检查
@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": settings.app_version
    }


# API v1 路由
app.include_router(
    api_v1_router,
    prefix="/api/v1",
    tags=["API v1"]
)


# 404 处理器
@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    """404错误处理"""
    return JSONResponse(
        status_code=404,
        content={
            "code": 404,
            "message": "请求的资源不存在",
            "timestamp": datetime.utcnow().isoformat()
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )
