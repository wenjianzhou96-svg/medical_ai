"""
医疗智能体系统 - 用户管理路由

提供用户的增删改查、密码管理、角色分配等接口
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from app.core.database import get_db
from app.models.user import User
from app.crud.user import UserCRUD
from app.services.auth import UserService, AuthService
from app.api.v1.deps import get_current_user
from app.core.exceptions import NotFoundException, BadRequestException

router = APIRouter()


# ============ Schema 定义 ============

class UserUpdate(BaseModel):
    """更新用户请求"""
    phone: Optional[str] = Field(None, description="手机号")
    email: Optional[str] = Field(None, description="邮箱")
    nickname: Optional[str] = Field(None, max_length=50, description="昵称")
    avatar_url: Optional[str] = Field(None, description="头像URL")
    gender: Optional[int] = Field(None, description="性别: 0-女, 1-男")
    birthday: Optional[str] = Field(None, description="生日")


class UserCreate(BaseModel):
    """创建用户请求（管理员用）"""
    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    password: str = Field(..., min_length=6, max_length=100, description="密码")
    phone: Optional[str] = Field(None, description="手机号")
    email: Optional[str] = Field(None, description="邮箱")
    nickname: Optional[str] = Field(None, description="昵称")
    gender: Optional[int] = Field(None, description="性别")
    avatar_url: Optional[str] = Field(None, description="头像URL")


class ChangePasswordRequest(BaseModel):
    """修改密码请求"""
    old_password: str = Field(..., description="旧密码")
    new_password: str = Field(..., min_length=6, max_length=100, description="新密码")


class ResetPasswordRequest(BaseModel):
    """重置密码请求（管理员用）"""
    new_password: str = Field(..., min_length=6, max_length=100, description="新密码")


class AssignRolesRequest(BaseModel):
    """分配角色请求"""
    role_ids: List[int] = Field(..., description="角色ID列表")


class UserResponse(BaseModel):
    """用户响应"""
    user_id: int
    username: str
    phone: Optional[str] = None
    email: Optional[str] = None
    avatar_url: Optional[str] = None
    nickname: Optional[str] = None
    gender: Optional[int] = None
    status: int
    created_at: str

    class Config:
        from_attributes = True


class UserDetailResponse(UserResponse):
    """用户详情响应（包含角色列表）"""
    roles: List[dict] = []


class UserListResponse(BaseModel):
    """用户列表响应"""
    list: List[dict]
    total: int
    page: int
    page_size: int


# ============ 路由 ============

@router.get("", response_model=UserListResponse, summary="获取用户列表")
async def get_users(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    username: Optional[str] = Query(None, description="用户名筛选"),
    phone: Optional[str] = Query(None, description="手机号筛选"),
    email: Optional[str] = Query(None, description="邮箱筛选"),
    status: Optional[int] = Query(None, description="状态筛选"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取用户列表
    
    - **page**: 页码，默认1
    - **page_size**: 每页数量，默认20，最大100
    - **username**: 用户名筛选（模糊匹配）
    - **phone**: 手机号筛选（模糊匹配）
    - **email**: 邮箱筛选（模糊匹配）
    - **status**: 状态筛选（0-禁用，1-启用）
    """
    skip = (page - 1) * page_size
    
    user_crud = UserCRUD()
    users, total = user_crud.get_list(
        db=db,
        skip=skip,
        limit=page_size,
        username=username,
        phone=phone,
        email=email,
        status=status
    )
    
    # 构建响应数据
    user_list = []
    for user in users:
        user_dict = {
            "user_id": user.user_id,
            "username": user.username,
            "phone": user.phone,
            "email": user.email,
            "nickname": user.nickname,
            "avatar_url": user.avatar_url,
            "gender": user.gender,
            "status": user.status,
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "last_login_at": user.last_login_at.isoformat() if user.last_login_at else None,
            "role_count": len(user.roles) if hasattr(user, 'roles') else 0
        }
        user_list.append(user_dict)
    
    return UserListResponse(
        list=user_list,
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/{user_id}", response_model=UserDetailResponse, summary="获取用户详情")
async def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取用户详情
    
    - **user_id**: 用户ID
    """
    user_crud = UserCRUD()
    user = user_crud.get_by_id(db, user_id)
    
    if not user:
        raise NotFoundException("用户", user_id)
    
    # 获取角色列表
    roles = []
    for role in user.roles:
        roles.append({
            "role_id": role.role_id,
            "role_name": role.role_name,
            "description": role.description
        })
    
    return UserDetailResponse(
        user_id=user.user_id,
        username=user.username,
        phone=user.phone,
        email=user.email,
        avatar_url=user.avatar_url,
        nickname=user.nickname,
        gender=user.gender,
        status=user.status,
        created_at=user.created_at.isoformat() if user.created_at else "",
        roles=roles
    )


@router.post("", response_model=UserResponse, summary="创建用户（管理员）")
async def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    创建用户（管理员操作）
    
    - **username**: 用户名（必填，3-50个字符）
    - **password**: 密码（必填，6-100个字符）
    - **phone**: 手机号（可选）
    - **email**: 邮箱（可选）
    - **nickname**: 昵称（可选）
    - **gender**: 性别（可选）
    - **avatar_url**: 头像URL（可选）
    """
    user_service = UserService(db)
    
    try:
        user = user_service.create_user(
            username=user_data.username,
            password=user_data.password,
            phone=user_data.phone,
            email=user_data.email,
            nickname=user_data.nickname,
            gender=user_data.gender,
            avatar_url=user_data.avatar_url
        )
    except Exception as e:
        raise BadRequestException(str(e))
    
    return UserResponse(
        user_id=user.user_id,
        username=user.username,
        phone=user.phone,
        email=user.email,
        avatar_url=user.avatar_url,
        nickname=user.nickname,
        gender=user.gender,
        status=user.status,
        created_at=user.created_at.isoformat() if user.created_at else ""
    )


@router.put("/{user_id}", response_model=UserResponse, summary="更新用户信息")
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    更新用户信息
    
    - **user_id**: 用户ID
    - **phone**: 手机号（可选）
    - **email**: 邮箱（可选）
    - **nickname**: 昵称（可选）
    - **avatar_url**: 头像URL（可选）
    - **gender**: 性别（可选）
    - **birthday**: 生日（可选）
    """
    # 检查权限：只有用户本人或管理员可以更新
    if current_user.user_id != user_id:
        # 简单检查是否是管理员（实际应检查角色权限）
        has_admin_role = any(role.role_name == 'admin' for role in current_user.roles)
        if not has_admin_role:
            raise BadRequestException("无权限更新此用户信息")
    
    user_service = UserService(db)
    
    # 转换birthday字符串
    update_data = user_data.model_dump(exclude_unset=True)
    if 'birthday' in update_data and update_data['birthday']:
        from datetime import datetime
        try:
            update_data['birthday'] = datetime.fromisoformat(update_data['birthday'])
        except:
            update_data.pop('birthday', None)
    
    try:
        user = user_service.update_user(user_id, **update_data)
    except Exception as e:
        raise NotFoundException("用户", user_id)
    
    return UserResponse(
        user_id=user.user_id,
        username=user.username,
        phone=user.phone,
        email=user.email,
        avatar_url=user.avatar_url,
        nickname=user.nickname,
        gender=user.gender,
        status=user.status,
        created_at=user.created_at.isoformat() if user.created_at else ""
    )


@router.delete("/{user_id}", summary="删除用户")
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    删除用户
    
    - **user_id**: 用户ID
    """
    user_service = UserService(db)
    
    try:
        result = user_service.delete_user(user_id)
    except Exception as e:
        raise BadRequestException(str(e))
    
    return result


@router.post("/{user_id}/change-password", summary="修改密码")
async def change_password(
    user_id: int,
    password_data: ChangePasswordRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    修改密码
    
    - **user_id**: 用户ID
    - **old_password**: 旧密码
    - **new_password**: 新密码
    """
    # 检查权限：只有用户本人可以修改密码
    if current_user.user_id != user_id:
        raise BadRequestException("无权限修改他人密码")
    
    auth_service = AuthService(db)
    
    try:
        result = auth_service.change_password(
            user_id=user_id,
            old_password=password_data.old_password,
            new_password=password_data.new_password
        )
    except Exception as e:
        raise BadRequestException(str(e))
    
    return result


@router.post("/{user_id}/reset-password", summary="重置密码（管理员）")
async def reset_password(
    user_id: int,
    password_data: ResetPasswordRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    重置密码（管理员操作）
    
    - **user_id**: 用户ID
    - **new_password**: 新密码
    """
    # 检查权限：只有管理员可以重置密码
    has_admin_role = any(role.role_name == 'admin' for role in current_user.roles)
    if not has_admin_role:
        raise BadRequestException("无权限重置用户密码")
    
    auth_service = AuthService(db)
    
    try:
        result = auth_service.reset_password(
            user_id=user_id,
            new_password=password_data.new_password,
            admin_id=current_user.user_id
        )
    except Exception as e:
        raise BadRequestException(str(e))
    
    return result


@router.post("/{user_id}/assign-roles", summary="分配角色")
async def assign_roles(
    user_id: int,
    role_data: AssignRolesRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    为用户分配角色
    
    - **user_id**: 用户ID
    - **role_ids**: 角色ID列表
    """
    user_service = UserService(db)
    
    try:
        result = user_service.assign_roles(user_id, role_data.role_ids)
    except Exception as e:
        raise BadRequestException(str(e))
    
    return result


@router.post("/{user_id}/enable", summary="启用用户")
async def enable_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    启用用户
    
    - **user_id**: 用户ID
    """
    user_service = UserService(db)
    
    try:
        user = user_service.update_user(user_id, status=1)
    except Exception as e:
        raise NotFoundException("用户", user_id)
    
    return {"message": "用户已启用"}


@router.post("/{user_id}/disable", summary="禁用用户")
async def disable_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    禁用用户
    
    - **user_id**: 用户ID
    """
    # 不能禁用自己
    if current_user.user_id == user_id:
        raise BadRequestException("不能禁用自己的账户")
    
    user_service = UserService(db)
    
    try:
        user = user_service.update_user(user_id, status=0)
    except Exception as e:
        raise NotFoundException("用户", user_id)
    
    return {"message": "用户已禁用"}


@router.get("/{user_id}/roles", summary="获取用户角色")
async def get_user_roles(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取用户的角色列表
    
    - **user_id**: 用户ID
    """
    user_service = UserService(db)
    
    try:
        roles = user_service.get_user_roles(user_id)
    except Exception as e:
        raise NotFoundException("用户", user_id)
    
    role_list = []
    for role in roles:
        role_list.append({
            "role_id": role.role_id,
            "role_name": role.role_name,
            "description": role.description,
            "status": role.status
        })
    
    return {"list": role_list}


@router.get("/{user_id}/permissions", summary="获取用户权限")
async def get_user_permissions(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取用户的权限列表
    
    - **user_id**: 用户ID
    """
    user_service = UserService(db)
    
    try:
        permissions = user_service.get_user_permissions(user_id)
    except Exception as e:
        raise NotFoundException("用户", user_id)
    
    return {"list": permissions}
