"""
医疗智能体系统 - 用户CRUD操作

提供用户的增删改查等数据库操作
"""

from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from app.models.user import User, Role, Permission, LoginLog
from app.core.security import get_password_hash, verify_password


class UserCRUD:
    """用户CRUD操作类"""

    @staticmethod
    def get_by_id(db: Session, user_id: int) -> Optional[User]:
        """根据用户ID获取用户"""
        return db.query(User).filter(User.user_id == user_id).first()

    @staticmethod
    def get_by_username(db: Session, username: str) -> Optional[User]:
        """根据用户名获取用户"""
        return db.query(User).filter(User.username == username).first()

    @staticmethod
    def get_by_phone(db: Session, phone: str) -> Optional[User]:
        """根据手机号获取用户"""
        return db.query(User).filter(User.phone == phone).first()

    @staticmethod
    def get_by_email(db: Session, email: str) -> Optional[User]:
        """根据邮箱获取用户"""
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_list(
        db: Session,
        skip: int = 0,
        limit: int = 20,
        username: Optional[str] = None,
        phone: Optional[str] = None,
        email: Optional[str] = None,
        status: Optional[int] = None
    ) -> tuple[List[User], int]:
        """获取用户列表"""
        query = db.query(User)

        # 构建过滤条件
        filters = []
        if username:
            filters.append(User.username.like(f"%{username}%"))
        if phone:
            filters.append(User.phone.like(f"%{phone}%"))
        if email:
            filters.append(User.email.like(f"%{email}%"))
        if status is not None:
            filters.append(User.status == status)

        if filters:
            query = query.filter(and_(*filters))

        # 获取总数
        total = query.count()

        # 分页查询
        users = query.order_by(User.created_at.desc()).offset(skip).limit(limit).all()

        return users, total

    @staticmethod
    def create(
        db: Session,
        username: str,
        password: str,
        phone: Optional[str] = None,
        email: Optional[str] = None,
        nickname: Optional[str] = None,
        gender: Optional[int] = None,
        avatar_url: Optional[str] = None
    ) -> User:
        """创建用户"""
        user = User(
            username=username,
            password_hash=get_password_hash(password),
            phone=phone,
            email=email,
            nickname=nickname,
            gender=gender,
            avatar_url=avatar_url,
            status=1
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def update(
        db: Session,
        user: User,
        **kwargs
    ) -> User:
        """更新用户"""
        for key, value in kwargs.items():
            if value is not None and hasattr(user, key):
                setattr(user, key, value)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def delete(db: Session, user_id: int) -> bool:
        """删除用户"""
        user = db.query(User).filter(User.user_id == user_id).first()
        if user:
            db.delete(user)
            db.commit()
            return True
        return False

    @staticmethod
    def update_password(db: Session, user: User, old_password: str, new_password: str) -> bool:
        """更新密码"""
        if not verify_password(old_password, user.password_hash):
            return False
        user.password_hash = get_password_hash(new_password)
        db.commit()
        return True

    @staticmethod
    def reset_password(db: Session, user_id: int, new_password: str) -> bool:
        """重置密码（管理员用）"""
        user = db.query(User).filter(User.user_id == user_id).first()
        if user:
            user.password_hash = get_password_hash(new_password)
            db.commit()
            return True
        return False

    @staticmethod
    def assign_roles(db: Session, user_id: int, role_ids: List[int]) -> bool:
        """分配角色"""
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            return False

        roles = db.query(Role).filter(Role.role_id.in_(role_ids)).all()
        user.roles = roles
        db.commit()
        return True


class RoleCRUD:
    """角色CRUD操作类"""

    @staticmethod
    def get_by_id(db: Session, role_id: int) -> Optional[Role]:
        """根据角色ID获取角色"""
        return db.query(Role).filter(Role.role_id == role_id).first()

    @staticmethod
    def get_by_name(db: Session, role_name: str) -> Optional[Role]:
        """根据角色名称获取角色"""
        return db.query(Role).filter(Role.role_name == role_name).first()

    @staticmethod
    def get_list(
        db: Session,
        skip: int = 0,
        limit: int = 20,
        status: Optional[int] = None
    ) -> tuple[List[Role], int]:
        """获取角色列表"""
        query = db.query(Role)

        if status is not None:
            query = query.filter(Role.status == status)

        total = query.count()
        roles = query.order_by(Role.created_at.desc()).offset(skip).limit(limit).all()

        return roles, total

    @staticmethod
    def create(
        db: Session,
        role_name: str,
        description: Optional[str] = None,
        status: int = 1
    ) -> Role:
        """创建角色"""
        role = Role(
            role_name=role_name,
            description=description,
            status=status
        )
        db.add(role)
        db.commit()
        db.refresh(role)
        return role

    @staticmethod
    def update(
        db: Session,
        role: Role,
        **kwargs
    ) -> Role:
        """更新角色"""
        for key, value in kwargs.items():
            if value is not None and hasattr(role, key):
                setattr(role, key, value)
        db.commit()
        db.refresh(role)
        return role

    @staticmethod
    def delete(db: Session, role_id: int) -> bool:
        """删除角色"""
        role = db.query(Role).filter(Role.role_id == role_id).first()
        if role:
            db.delete(role)
            db.commit()
            return True
        return False


class PermissionCRUD:
    """权限CRUD操作类"""

    @staticmethod
    def get_by_id(db: Session, permission_id: int) -> Optional[Permission]:
        """根据权限ID获取权限"""
        return db.query(Permission).filter(Permission.permission_id == permission_id).first()

    @staticmethod
    def get_by_resource_action(db: Session, resource: str, action: str) -> Optional[Permission]:
        """根据资源和操作获取权限"""
        return db.query(Permission).filter(
            and_(
                Permission.resource == resource,
                Permission.action == action
            )
        ).first()

    @staticmethod
    def get_list(
        db: Session,
        skip: int = 0,
        limit: int = 20,
        resource: Optional[str] = None
    ) -> tuple[List[Permission], int]:
        """获取权限列表"""
        query = db.query(Permission)

        if resource:
            query = query.filter(Permission.resource.like(f"%{resource}%"))

        total = query.count()
        permissions = query.order_by(Permission.created_at.desc()).offset(skip).limit(limit).all()

        return permissions, total

    @staticmethod
    def create(
        db: Session,
        permission_name: str,
        resource: str,
        action: str,
        description: Optional[str] = None
    ) -> Permission:
        """创建权限"""
        permission = Permission(
            permission_name=permission_name,
            resource=resource,
            action=action,
            description=description
        )
        db.add(permission)
        db.commit()
        db.refresh(permission)
        return permission

    @staticmethod
    def update(
        db: Session,
        permission: Permission,
        **kwargs
    ) -> Permission:
        """更新权限"""
        for key, value in kwargs.items():
            if value is not None and hasattr(permission, key):
                setattr(permission, key, value)
        db.commit()
        db.refresh(permission)
        return permission

    @staticmethod
    def delete(db: Session, permission_id: int) -> bool:
        """删除权限"""
        permission = db.query(Permission).filter(Permission.permission_id == permission_id).first()
        if permission:
            db.delete(permission)
            db.commit()
            return True
        return False


class LoginLogCRUD:
    """登录日志CRUD操作类"""

    @staticmethod
    def create(
        db: Session,
        user_id: int,
        login_type: str,
        login_status: int,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        device_info: Optional[str] = None,
        failure_reason: Optional[str] = None
    ) -> LoginLog:
        """创建登录日志"""
        login_log = LoginLog(
            user_id=user_id,
            login_type=login_type,
            login_status=login_status,
            ip_address=ip_address,
            user_agent=user_agent,
            device_info=device_info,
            failure_reason=failure_reason
        )
        db.add(login_log)
        db.commit()
        db.refresh(login_log)
        return login_log

    @staticmethod
    def get_list(
        db: Session,
        user_id: Optional[int] = None,
        login_status: Optional[int] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        skip: int = 0,
        limit: int = 20
    ) -> tuple[List[LoginLog], int]:
        """获取登录日志列表"""
        query = db.query(LoginLog)

        filters = []
        if user_id:
            filters.append(LoginLog.user_id == user_id)
        if login_status is not None:
            filters.append(LoginLog.login_status == login_status)

        if filters:
            query = query.filter(and_(*filters))

        total = query.count()
        logs = query.order_by(LoginLog.created_at.desc()).offset(skip).limit(limit).all()

        return logs, total
