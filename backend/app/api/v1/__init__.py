"""
医疗智能体系统 - API路由
"""

from fastapi import APIRouter
from app.api.v1 import (
    auth,
    users,
    roles,
    permissions,
    consultations,
    health,
    articles,
    doctors,
    knowledge,
    notifications,
    system
)

# 创建API v1路由，禁用尾部斜杠重定向
router = APIRouter(redirect_slashes=False)

# 注册各个模块路由
router.include_router(auth.router, prefix="/auth", tags=["认证"])
router.include_router(users.router, prefix="/users", tags=["用户"])
router.include_router(roles.router, prefix="/roles", tags=["角色"])
router.include_router(permissions.router, prefix="/permissions", tags=["权限"])
router.include_router(consultations.router, prefix="/consultations", tags=["问诊"])
router.include_router(health.router, prefix="/health", tags=["健康"])
router.include_router(articles.router, prefix="/articles", tags=["文章"])
router.include_router(doctors.router, prefix="/doctors", tags=["医生"])
router.include_router(knowledge.router, prefix="/knowledge", tags=["知识库"])
router.include_router(notifications.router, prefix="/notifications", tags=["通知"])
router.include_router(system.router, prefix="/system", tags=["系统"])
