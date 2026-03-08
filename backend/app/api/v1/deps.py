"""
医疗智能体系统 - API依赖注入

提供通用的依赖注入函数和权限验证装饰器
"""

from typing import Optional, List
from functools import wraps
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import verify_token
from app.core.exceptions import UnauthorizedException, ForbiddenException
from app.models.user import User, Role, Permission

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    获取当前登录用户
    
    Args:
        token: JWT令牌
        db: 数据库会话
    
    Returns:
        User: 当前用户对象
    
    Raises:
        UnauthorizedException: 未授权异常
    """
    # 验证令牌
    payload = verify_token(token)
    
    if not payload:
        raise UnauthorizedException("无效的令牌或令牌已过期")
    
    # 获取用户ID
    user_id = payload.get("sub")
    if not user_id:
        raise UnauthorizedException("无效的令牌")
    
    # 查询用户
    user = db.query(User).filter(User.user_id == int(user_id)).first()
    
    if not user:
        raise UnauthorizedException("用户不存在")
    
    # 检查用户状态
    if user.status != 1:
        raise UnauthorizedException("账户已被禁用")
    
    # 加载用户的角色和权限
    # 使用eager loading避免N+1问题
    user.roles  # 加载角色
    
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    获取当前活跃用户
    
    Args:
        current_user: 当前用户
    
    Returns:
        User: 当前用户对象
    
    Raises:
        UnauthorizedException: 用户未激活
    """
    if current_user.status != 1:
        raise UnauthorizedException("用户账户已被禁用")
    return current_user


async def get_current_user_optional(
    token: Optional[str] = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    获取当前用户（可选，不强制）
    
    Args:
        token: JWT令牌
        db: 数据库会话
    
    Returns:
        Optional[User]: 用户对象，如果未登录则返回None
    """
    if not token:
        return None
    
    try:
        return await get_current_user(token, db)
    except:
        return None


# ============ 权限验证函数 ============

def check_role(required_roles: List[str]):
    """
    角色检查装饰器工厂
    
    Args:
        required_roles: 需要的角色列表
    
    Returns:
        装饰器函数
    """
    def role_checker(current_user: User = Depends(get_current_user)):
        # 加载用户的角色
        user_roles = current_user.roles
        
        # 获取用户角色名列表
        user_role_names = [role.role_name for role in user_roles]
        
        # 检查是否具有所需角色
        for required_role in required_roles:
            if required_role in user_role_names:
                return current_user
        
        # 没有权限
        raise ForbiddenException(f"需要角色: {', '.join(required_roles)}")
    
    return role_checker


def check_permission(required_permissions: List[str]):
    """
    权限检查装饰器工厂
    
    Args:
        required_permissions: 需要的权限列表，格式: "resource:action"
    
    Returns:
        装饰器函数
    """
    def permission_checker(current_user: User = Depends(get_current_user)):
        # 加载用户的角色和权限
        user_roles = current_user.roles
        
        # 收集用户所有权限
        user_permissions = set()
        for role in user_roles:
            role.permissions  # 加载角色的权限
            for perm in role.permissions:
                user_permissions.add(f"{perm.resource}:{perm.action}")
        
        # 检查是否具有所需权限
        for required_perm in required_permissions:
            if required_perm in user_permissions:
                return current_user
        
        # 没有权限
        raise ForbiddenException(f"需要权限: {', '.join(required_permissions)}")
    
    return permission_checker


async def require_admin(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    要求管理员权限
    
    Args:
        current_user: 当前用户
    
    Returns:
        User: 当前用户对象
    
    Raises:
        ForbiddenException: 非管理员用户
    """
    # 加载用户的角色
    user_roles = current_user.roles
    
    # 检查是否具有admin角色
    for role in user_roles:
        if role.role_name == "admin" and role.status == 1:
            return current_user
    
    raise ForbiddenException("需要管理员权限")


async def require_roles(
    required_roles: List[str],
    current_user: User = Depends(get_current_user)
) -> User:
    """
    要求特定角色
    
    Args:
        required_roles: 需要的角色列表
        current_user: 当前用户
    
    Returns:
        User: 当前用户对象
    
    Raises:
        ForbiddenException: 角色不匹配
    """
    # 加载用户的角色
    user_roles = current_user.roles
    
    # 获取用户角色名列表
    user_role_names = [role.role_name for role in user_roles if role.status == 1]
    
    # 检查是否具有所需角色
    for required_role in required_roles:
        if required_role in user_role_names:
            return current_user
    
    raise ForbiddenException(f"需要以下角色之一: {', '.join(required_roles)}")


async def require_permissions(
    required_permissions: List[str],
    current_user: User = Depends(get_current_user)
) -> User:
    """
    要求特定权限
    
    Args:
        required_permissions: 需要的权限列表，格式: "resource:action"
        current_user: 当前用户
    
    Returns:
        User: 当前用户对象
    
    Raises:
        ForbiddenException: 权限不足
    """
    # 加载用户的角色和权限
    user_roles = current_user.roles
    
    # 收集用户所有权限
    user_permissions = set()
    for role in user_roles:
        if role.status != 1:  # 跳过禁用的角色
            continue
        role.permissions  # 加载角色的权限
        for perm in role.permissions:
            user_permissions.add(f"{perm.resource}:{perm.action}")
    
    # 检查是否具有所需权限
    for required_perm in required_permissions:
        if required_perm in user_permissions:
            return current_user
    
    raise ForbiddenException(f"需要以下权限之一: {', '.join(required_permissions)}")


async def check_permissions(
    required_permissions: List[str],
    current_user: User = Depends(get_current_user)
) -> bool:
    """
    异步检查权限（用于API端点内部调用）
    
    Args:
        required_permissions: 需要的权限列表，格式: "resource:action"
        current_user: 当前用户
    
    Returns:
        bool: 权限检查是否通过
    
    Raises:
        ForbiddenException: 权限不足
    """
    # 加载用户的角色和权限
    user_roles = current_user.roles
    
    # 收集用户所有权限
    user_permissions = set()
    for role in user_roles:
        if role.status != 1:  # 跳过禁用的角色
            continue
        role.permissions  # 加载角色的权限
        for perm in role.permissions:
            user_permissions.add(f"{perm.resource}:{perm.action}")
    
    # 检查是否具有所需权限
    for required_perm in required_permissions:
        if required_perm in user_permissions:
            return True
    
    raise ForbiddenException(f"需要以下权限之一: {', '.join(required_permissions)}")
