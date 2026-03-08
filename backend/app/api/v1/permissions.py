"""
医疗智能体系统 - 权限管理路由

提供权限的增删改查等接口
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from app.core.database import get_db
from app.models.user import Permission, User
from app.crud.user import PermissionCRUD
from app.api.v1.deps import get_current_user
from app.core.exceptions import NotFoundException, BadRequestException

router = APIRouter()


# ============ Schema 定义 ============

class PermissionCreate(BaseModel):
    """创建权限请求"""
    permission_name: str = Field(..., min_length=2, max_length=100, description="权限名称")
    resource: str = Field(..., max_length=50, description="资源名称")
    action: str = Field(..., max_length=50, description="操作类型")
    description: Optional[str] = Field(None, max_length=255, description="权限描述")


class PermissionUpdate(BaseModel):
    """更新权限请求"""
    permission_name: Optional[str] = Field(None, min_length=2, max_length=100, description="权限名称")
    resource: Optional[str] = Field(None, max_length=50, description="资源名称")
    action: Optional[str] = Field(None, max_length=50, description="操作类型")
    description: Optional[str] = Field(None, max_length=255, description="权限描述")


class PermissionResponse(BaseModel):
    """权限响应"""
    permission_id: int
    permission_name: str
    resource: str
    action: str
    description: Optional[str] = None
    created_at: str

    class Config:
        from_attributes = True


class PermissionDetailResponse(PermissionResponse):
    """权限详情响应（包含角色数）"""
    role_count: int = 0


# ============ 路由 ============

@router.get("", response_model=dict, summary="获取权限列表")
async def get_permissions(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    resource: Optional[str] = Query(None, description="资源筛选"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取权限列表
    
    - **page**: 页码，默认1
    - **page_size**: 每页数量，默认20，最大100
    - **resource**: 资源名称筛选（模糊匹配）
    """
    skip = (page - 1) * page_size
    
    perm_crud = PermissionCRUD()
    permissions, total = perm_crud.get_list(
        db=db,
        skip=skip,
        limit=page_size,
        resource=resource
    )
    
    # 构建响应数据
    perm_list = []
    for perm in permissions:
        perm_dict = {
            "permission_id": perm.permission_id,
            "permission_name": perm.permission_name,
            "resource": perm.resource,
            "action": perm.action,
            "description": perm.description,
            "created_at": perm.created_at.isoformat() if perm.created_at else None,
            "role_count": len(perm.roles) if hasattr(perm, 'roles') else 0
        }
        perm_list.append(perm_dict)
    
    return {
        "list": perm_list,
        "total": total,
        "page": page,
        "page_size": page_size
    }


@router.get("/{permission_id}", response_model=PermissionDetailResponse, summary="获取权限详情")
async def get_permission(
    permission_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取权限详情
    
    - **permission_id**: 权限ID
    """
    perm_crud = PermissionCRUD()
    permission = perm_crud.get_by_id(db, permission_id)
    
    if not permission:
        raise NotFoundException("权限", permission_id)
    
    return PermissionDetailResponse(
        permission_id=permission.permission_id,
        permission_name=permission.permission_name,
        resource=permission.resource,
        action=permission.action,
        description=permission.description,
        created_at=permission.created_at.isoformat() if permission.created_at else "",
        role_count=len(permission.roles) if hasattr(permission, 'roles') else 0
    )


@router.post("", response_model=PermissionResponse, summary="创建权限")
async def create_permission(
    perm_data: PermissionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    创建权限
    
    - **permission_name**: 权限名称（必填，2-100个字符）
    - **resource**: 资源名称（必填，如：user, consultation, health等）
    - **action**: 操作类型（必填，如：create, read, update, delete等）
    - **description**: 权限描述（可选）
    """
    perm_crud = PermissionCRUD()
    
    # 检查权限是否已存在（根据资源+操作）
    existing_perm = perm_crud.get_by_resource_action(db, perm_data.resource, perm_data.action)
    if existing_perm:
        raise BadRequestException(f"权限已存在：{perm_data.resource}:{perm_data.action}")
    
    # 检查权限名称是否已存在
    existing_name = perm_crud.get_by_id(db, perm_data.permission_name)
    if existing_name:
        raise BadRequestException("权限名称已存在")
    
    # 创建权限
    permission = perm_crud.create(
        db=db,
        permission_name=perm_data.permission_name,
        resource=perm_data.resource,
        action=perm_data.action,
        description=perm_data.description
    )
    
    return PermissionResponse(
        permission_id=permission.permission_id,
        permission_name=permission.permission_name,
        resource=permission.resource,
        action=permission.action,
        description=permission.description,
        created_at=permission.created_at.isoformat() if permission.created_at else ""
    )


@router.put("/{permission_id}", response_model=PermissionResponse, summary="更新权限")
async def update_permission(
    permission_id: int,
    perm_data: PermissionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    更新权限
    
    - **permission_id**: 权限ID
    - **permission_name**: 权限名称（可选）
    - **resource**: 资源名称（可选）
    - **action**: 操作类型（可选）
    - **description**: 权限描述（可选）
    """
    perm_crud = PermissionCRUD()
    
    # 检查权限是否存在
    permission = perm_crud.get_by_id(db, permission_id)
    if not permission:
        raise NotFoundException("权限", permission_id)
    
    # 如果更新资源+操作，检查是否已存在
    if perm_data.resource and perm_data.action:
        existing_perm = perm_crud.get_by_resource_action(db, perm_data.resource, perm_data.action)
        if existing_perm and existing_perm.permission_id != permission_id:
            raise BadRequestException(f"权限已存在：{perm_data.resource}:{perm_data.action}")
    
    # 更新权限
    update_data = perm_data.model_dump(exclude_unset=True)
    permission = perm_crud.update(db, permission, **update_data)
    
    return PermissionResponse(
        permission_id=permission.permission_id,
        permission_name=permission.permission_name,
        resource=permission.resource,
        action=permission.action,
        description=permission.description,
        created_at=permission.created_at.isoformat() if permission.created_at else ""
    )


@router.delete("/{permission_id}", summary="删除权限")
async def delete_permission(
    permission_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    删除权限
    
    - **permission_id**: 权限ID
    """
    perm_crud = PermissionCRUD()
    
    # 检查权限是否存在
    permission = perm_crud.get_by_id(db, permission_id)
    if not permission:
        raise NotFoundException("权限", permission_id)
    
    # 检查是否有关联角色
    if permission.roles:
        raise BadRequestException("该权限已分配给角色，无法删除")
    
    # 删除权限
    success = perm_crud.delete(db, permission_id)
    if not success:
        raise BadRequestException("权限删除失败")
    
    return {"message": "权限删除成功"}


@router.get("/resources/list", response_model=dict, summary="获取资源列表")
async def get_resources(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取所有资源列表（用于权限配置）
    
    返回系统中所有可能的资源类型
    """
    resources = [
        {"value": "user", "label": "用户管理"},
        {"value": "role", "label": "角色管理"},
        {"value": "permission", "label": "权限管理"},
        {"value": "consultation", "label": "问诊管理"},
        {"value": "health", "label": "健康管理"},
        {"value": "article", "label": "文章管理"},
        {"value": "comment", "label": "评论管理"},
        {"value": "doctor", "label": "医生管理"},
        {"value": "knowledge", "label": "知识库管理"},
        {"value": "notification", "label": "消息通知"},
        {"value": "system", "label": "系统管理"},
    ]
    
    return {"list": resources}


@router.get("/actions/list", response_model=dict, summary="获取操作类型列表")
async def get_actions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取所有操作类型列表（用于权限配置）
    
    返回系统中所有可能的操作类型
    """
    actions = [
        {"value": "create", "label": "创建"},
        {"value": "read", "label": "查看"},
        {"value": "update", "label": "更新"},
        {"value": "delete", "label": "删除"},
        {"value": "export", "label": "导出"},
        {"value": "import", "label": "导入"},
        {"value": "audit", "label": "审核"},
        {"value": "assign", "label": "分配"},
    ]
    
    return {"list": actions}
