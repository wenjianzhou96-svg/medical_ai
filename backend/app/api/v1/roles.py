"""
医疗智能体系统 - 角色管理路由

提供角色的增删改查等接口
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from app.core.database import get_db
from app.models.user import Role, User
from app.crud.user import RoleCRUD, UserCRUD
from app.api.v1.deps import get_current_user
from app.core.exceptions import NotFoundException, BadRequestException

router = APIRouter()


# ============ Schema 定义 ============

class RoleCreate(BaseModel):
    """创建角色请求"""
    role_name: str = Field(..., min_length=2, max_length=50, description="角色名称")
    description: Optional[str] = Field(None, max_length=255, description="角色描述")
    status: int = Field(1, description="状态: 0-禁用, 1-启用")


class RoleUpdate(BaseModel):
    """更新角色请求"""
    role_name: Optional[str] = Field(None, min_length=2, max_length=50, description="角色名称")
    description: Optional[str] = Field(None, max_length=255, description="角色描述")
    status: Optional[int] = Field(None, description="状态: 0-禁用, 1-启用")


class RoleResponse(BaseModel):
    """角色响应"""
    role_id: int
    role_name: str
    description: Optional[str] = None
    status: int
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


class RoleDetailResponse(RoleResponse):
    """角色详情响应（包含用户数和权限数）"""
    user_count: int = 0
    permission_count: int = 0


class AssignPermissionsRequest(BaseModel):
    """分配权限请求"""
    permission_ids: List[int] = Field(..., description="权限ID列表")


class RoleWithPermissionsResponse(RoleResponse):
    """角色详情（包含权限列表）"""
    permissions: List[dict] = []


# ============ 路由 ============

@router.get("", response_model=dict, summary="获取角色列表")
async def get_roles(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    status: Optional[int] = Query(None, description="状态筛选"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取角色列表
    
    - **page**: 页码，默认1
    - **page_size**: 每页数量，默认20，最大100
    - **status**: 状态筛选（0-禁用，1-启用）
    """
    skip = (page - 1) * page_size
    
    role_crud = RoleCRUD()
    roles, total = role_crud.get_list(
        db=db,
        skip=skip,
        limit=page_size,
        status=status
    )
    
    # 构建响应数据
    role_list = []
    for role in roles:
        role_dict = {
            "role_id": role.role_id,
            "role_name": role.role_name,
            "description": role.description,
            "status": role.status,
            "created_at": role.created_at.isoformat() if role.created_at else None,
            "updated_at": role.updated_at.isoformat() if role.updated_at else None,
            "user_count": len(role.users) if hasattr(role, 'users') else 0,
            "permission_count": len(role.permissions) if hasattr(role, 'permissions') else 0
        }
        role_list.append(role_dict)
    
    return {
        "list": role_list,
        "total": total,
        "page": page,
        "page_size": page_size
    }


@router.get("/{role_id}", response_model=RoleWithPermissionsResponse, summary="获取角色详情")
async def get_role(
    role_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取角色详情
    
    - **role_id**: 角色ID
    """
    role_crud = RoleCRUD()
    role = role_crud.get_by_id(db, role_id)
    
    if not role:
        raise NotFoundException("角色", role_id)
    
    # 获取权限列表
    permissions = []
    for perm in role.permissions:
        permissions.append({
            "permission_id": perm.permission_id,
            "permission_name": perm.permission_name,
            "resource": perm.resource,
            "action": perm.action,
            "description": perm.description
        })
    
    return RoleWithPermissionsResponse(
        role_id=role.role_id,
        role_name=role.role_name,
        description=role.description,
        status=role.status,
        created_at=role.created_at.isoformat() if role.created_at else "",
        updated_at=role.updated_at.isoformat() if role.updated_at else "",
        permissions=permissions
    )


@router.post("", response_model=RoleResponse, summary="创建角色")
async def create_role(
    role_data: RoleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    创建角色
    
    - **role_name**: 角色名称（必填，2-50个字符）
    - **description**: 角色描述（可选）
    - **status**: 状态（默认1启用）
    """
    role_crud = RoleCRUD()
    
    # 检查角色名是否已存在
    existing_role = role_crud.get_by_name(db, role_data.role_name)
    if existing_role:
        raise BadRequestException("角色名称已存在")
    
    # 创建角色
    role = role_crud.create(
        db=db,
        role_name=role_data.role_name,
        description=role_data.description,
        status=role_data.status
    )
    
    return RoleResponse(
        role_id=role.role_id,
        role_name=role.role_name,
        description=role.description,
        status=role.status,
        created_at=role.created_at.isoformat() if role.created_at else "",
        updated_at=role.updated_at.isoformat() if role.updated_at else ""
    )


@router.put("/{role_id}", response_model=RoleResponse, summary="更新角色")
async def update_role(
    role_id: int,
    role_data: RoleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    更新角色
    
    - **role_id**: 角色ID
    - **role_name**: 角色名称（可选）
    - **description**: 角色描述（可选）
    - **status**: 状态（可选）
    """
    role_crud = RoleCRUD()
    
    # 检查角色是否存在
    role = role_crud.get_by_id(db, role_id)
    if not role:
        raise NotFoundException("角色", role_id)
    
    # 如果更新角色名，检查是否已存在
    if role_data.role_name and role_data.role_name != role.role_name:
        existing_role = role_crud.get_by_name(db, role_data.role_name)
        if existing_role:
            raise BadRequestException("角色名称已存在")
    
    # 更新角色
    update_data = role_data.model_dump(exclude_unset=True)
    role = role_crud.update(db, role, **update_data)
    
    return RoleResponse(
        role_id=role.role_id,
        role_name=role.role_name,
        description=role.description,
        status=role.status,
        created_at=role.created_at.isoformat() if role.created_at else "",
        updated_at=role.updated_at.isoformat() if role.updated_at else ""
    )


@router.delete("/{role_id}", summary="删除角色")
async def delete_role(
    role_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    删除角色
    
    - **role_id**: 角色ID
    """
    role_crud = RoleCRUD()
    
    # 检查角色是否存在
    role = role_crud.get_by_id(db, role_id)
    if not role:
        raise NotFoundException("角色", role_id)
    
    # 检查是否有关联用户
    if role.users:
        raise BadRequestException("该角色下存在用户，无法删除")
    
    # 删除角色
    success = role_crud.delete(db, role_id)
    if not success:
        raise BadRequestException("角色删除失败")
    
    return {"message": "角色删除成功"}


@router.post("/{role_id}/permissions", summary="分配权限")
async def assign_permissions(
    role_id: int,
    request: AssignPermissionsRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    为角色分配权限
    
    - **role_id**: 角色ID
    - **permission_ids**: 权限ID列表
    """
    from app.crud.user import PermissionCRUD
    
    role_crud = RoleCRUD()
    perm_crud = PermissionCRUD()
    
    # 检查角色是否存在
    role = role_crud.get_by_id(db, role_id)
    if not role:
        raise NotFoundException("角色", role_id)
    
    # 检查权限是否存在
    permissions = []
    for perm_id in request.permission_ids:
        perm = perm_crud.get_by_id(db, perm_id)
        if not perm:
            raise NotFoundException("权限", perm_id)
        permissions.append(perm)
    
    # 分配权限
    role.permissions = permissions
    db.commit()
    db.refresh(role)
    
    return {"message": "权限分配成功"}


@router.get("/{role_id}/users", summary="获取角色下的用户列表")
async def get_role_users(
    role_id: int,
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取角色下的用户列表
    
    - **role_id**: 角色ID
    """
    role_crud = RoleCRUD()
    
    # 检查角色是否存在
    role = role_crud.get_by_id(db, role_id)
    if not role:
        raise NotFoundException("角色", role_id)
    
    # 获取用户列表
    users = role.users
    total = len(users)
    
    # 分页
    start = (page - 1) * page_size
    end = start + page_size
    page_users = users[start:end]
    
    user_list = []
    for user in page_users:
        user_list.append({
            "user_id": user.user_id,
            "username": user.username,
            "phone": user.phone,
            "email": user.email,
            "nickname": user.nickname,
            "status": user.status
        })
    
    return {
        "list": user_list,
        "total": total,
        "page": page,
        "page_size": page_size
    }
