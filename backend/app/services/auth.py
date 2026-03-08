"""
医疗智能体系统 - 用户服务层

提供用户注册、登录、权限验证等业务逻辑
"""

from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.models.user import User, Role, Permission, LoginLog
from app.crud.user import UserCRUD, RoleCRUD, PermissionCRUD, LoginLogCRUD
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    create_refresh_token,
    verify_token
)
from app.core.exceptions import (
    BadRequestException,
    UnauthorizedException,
    NotFoundException,
    ForbiddenException
)


class AuthService:
    """认证服务类"""

    # Token过期时间配置
    ACCESS_TOKEN_EXPIRE_MINUTES = 120
    REFRESH_TOKEN_EXPIRE_DAYS = 7

    def __init__(self, db: Session):
        """初始化认证服务"""
        self.db = db
        self.user_crud = UserCRUD()

    def register(
        self,
        username: str,
        password: str,
        phone: Optional[str] = None,
        email: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        用户注册

        Args:
            username: 用户名
            password: 密码
            phone: 手机号
            email: 邮箱

        Returns:
            包含token和用户信息的字典
        """
        # 检查用户名是否已存在
        existing_user = self.user_crud.get_by_username(self.db, username)
        if existing_user:
            raise BadRequestException("用户名已存在")

        # 检查手机号是否已存在
        if phone:
            existing_phone = self.user_crud.get_by_phone(self.db, phone)
            if existing_phone:
                raise BadRequestException("手机号已被注册")

        # 检查邮箱是否已存在
        if email:
            existing_email = self.user_crud.get_by_email(self.db, email)
            if existing_email:
                raise BadRequestException("邮箱已被注册")

        # 创建用户
        user = self.user_crud.create(
            db=self.db,
            username=username,
            password=password,
            phone=phone,
            email=email
        )

        # 生成Token
        tokens = self._generate_tokens(user)

        return {
            "token": tokens,
            "user": self._format_user(user)
        }

    def login(
        self,
        username: str,
        password: str,
        login_type: str = "password",
        ip_address: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        用户登录

        Args:
            username: 用户名
            password: 密码
            login_type: 登录类型
            ip_address: IP地址

        Returns:
            包含token和用户信息的字典
        """
        # 查找用户
        user = self.user_crud.get_by_username(self.db, username)
        if not user:
            # 记录登录失败日志
            self._create_login_log(
                user_id=None,
                login_type=login_type,
                login_status=0,
                ip_address=ip_address,
                failure_reason="用户不存在"
            )
            raise UnauthorizedException("用户名或密码错误")

        # 验证密码
        if not verify_password(password, user.password_hash):
            # 记录登录失败日志
            self._create_login_log(
                user_id=user.user_id,
                login_type=login_type,
                login_status=0,
                ip_address=ip_address,
                failure_reason="密码错误"
            )
            raise UnauthorizedException("用户名或密码错误")

        # 检查用户状态
        if user.status != 1:
            self._create_login_log(
                user_id=user.user_id,
                login_type=login_type,
                login_status=0,
                ip_address=ip_address,
                failure_reason="账户已被禁用"
            )
            raise UnauthorizedException("账户已被禁用")

        # 更新最后登录时间
        user.last_login_at = datetime.utcnow()
        self.db.commit()

        # 记录登录成功日志
        self._create_login_log(
            user_id=user.user_id,
            login_type=login_type,
            login_status=1,
            ip_address=ip_address
        )

        # 生成Token
        tokens = self._generate_tokens(user)

        return {
            "token": tokens,
            "user": self._format_user(user)
        }

    def refresh_token(self, refresh_token: str) -> Dict[str, Any]:
        """
        刷新Token

        Args:
            refresh_token: 刷新令牌

        Returns:
            新的token信息
        """
        # 验证刷新令牌
        payload = verify_token(refresh_token)
        if not payload:
            raise UnauthorizedException("无效的刷新令牌")

        # 获取用户
        user_id = payload.get("sub")
        user = self.user_crud.get_by_id(self.db, int(user_id))

        if not user or user.status != 1:
            raise UnauthorizedException("用户不存在或已被禁用")

        # 生成新Token
        tokens = self._generate_tokens(user)

        return tokens

    def logout(self, user_id: int) -> Dict[str, str]:
        """
        用户登出

        Args:
            user_id: 用户ID

        Returns:
            登出结果
        """
        # 在实际应用中，可能需要将令牌加入黑名单
        return {"message": "登出成功"}

    def change_password(
        self,
        user_id: int,
        old_password: str,
        new_password: str
    ) -> Dict[str, str]:
        """
        修改密码

        Args:
            user_id: 用户ID
            old_password: 旧密码
            new_password: 新密码

        Returns:
            修改结果
        """
        user = self.user_crud.get_by_id(self.db, user_id)
        if not user:
            raise NotFoundException("用户", user_id)

        # 验证旧密码
        if not verify_password(old_password, user.password_hash):
            raise BadRequestException("原密码错误")

        # 更新密码
        self.user_crud.update_password(self.db, user, old_password, new_password)

        return {"message": "密码修改成功"}

    def reset_password(
        self,
        user_id: int,
        new_password: str,
        admin_id: Optional[int] = None
    ) -> Dict[str, str]:
        """
        重置密码（管理员用）

        Args:
            user_id: 用户ID
            new_password: 新密码
            admin_id: 管理员ID

        Returns:
            重置结果
        """
        # 检查用户是否存在
        user = self.user_crud.get_by_id(self.db, user_id)
        if not user:
            raise NotFoundException("用户", user_id)

        # 重置密码
        self.user_crud.reset_password(self.db, user_id, new_password)

        return {"message": "密码重置成功"}

    def _generate_tokens(self, user: User) -> Dict[str, Any]:
        """生成访问令牌和刷新令牌"""
        access_token = create_access_token(
            data={
                "sub": str(user.user_id),
                "username": user.username
            }
        )
        refresh_token = create_refresh_token(
            data={"sub": str(user.user_id)}
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": self.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        }

    def _format_user(self, user: User) -> Dict[str, Any]:
        """格式化用户信息"""
        return {
            "user_id": user.user_id,
            "username": user.username,
            "phone": user.phone,
            "email": user.email,
            "avatar_url": user.avatar_url,
            "nickname": user.nickname,
            "gender": user.gender,
            "status": user.status
        }

    def _create_login_log(
        self,
        user_id: Optional[int],
        login_type: str,
        login_status: int,
        ip_address: Optional[str] = None,
        failure_reason: Optional[str] = None
    ):
        """创建登录日志"""
        LoginLogCRUD.create(
            db=self.db,
            user_id=user_id,
            login_type=login_type,
            login_status=login_status,
            ip_address=ip_address,
            failure_reason=failure_reason
        )


    def create_user(
        self,
        username: str,
        password: str,
        phone: Optional[str] = None,
        email: Optional[str] = None,
        nickname: Optional[str] = None,
        gender: Optional[int] = None,
        avatar_url: Optional[str] = None
    ) -> User:
        """
        创建用户（管理员用）

        Args:
            username: 用户名
            password: 密码
            phone: 手机号
            email: 邮箱
            nickname: 昵称
            gender: 性别
            avatar_url: 头像URL

        Returns:
            用户对象
        """
        # 检查用户名是否已存在
        existing_user = self.user_crud.get_by_username(self.db, username)
        if existing_user:
            raise BadRequestException("用户名已存在")

        # 检查手机号是否已存在
        if phone:
            existing_phone = self.user_crud.get_by_phone(self.db, phone)
            if existing_phone:
                raise BadRequestException("手机号已被注册")

        # 检查邮箱是否已存在
        if email:
            existing_email = self.user_crud.get_by_email(self.db, email)
            if existing_email:
                raise BadRequestException("邮箱已被注册")

        # 创建用户
        return self.user_crud.create(
            db=self.db,
            username=username,
            password=password,
            phone=phone,
            email=email,
            nickname=nickname,
            gender=gender,
            avatar_url=avatar_url
        )


    def get_user(self, user_id: int) -> User:
        """
        获取用户详情

        Args:
            user_id: 用户ID

        Returns:
            用户对象
        """
        user = self.user_crud.get_by_id(self.db, user_id)
        if not user:
            raise NotFoundException("用户", user_id)
        return user

    def get_user_list(
        self,
        skip: int = 0,
        limit: int = 20,
        username: Optional[str] = None,
        phone: Optional[str] = None,
        email: Optional[str] = None,
        status: Optional[int] = None
    ) -> tuple[List[User], int]:
        """
        获取用户列表

        Args:
            skip: 跳过条数
            limit: 限制条数
            username: 用户名（模糊查询）
            phone: 手机号（模糊查询）
            email: 邮箱（模糊查询）
            status: 状态

        Returns:
            (用户列表, 总数)元组
        """
        return self.user_crud.get_list(
            db=self.db,
            skip=skip,
            limit=limit,
            username=username,
            phone=phone,
            email=email,
            status=status
        )

    def update_user(
        self,
        user_id: int,
        **kwargs
    ) -> User:
        """
        更新用户信息

        Args:
            user_id: 用户ID
            **kwargs: 更新的字段

        Returns:
            更新后的用户对象
        """
        user = self.user_crud.get_by_id(self.db, user_id)
        if not user:
            raise NotFoundException("用户", user_id)

        return self.user_crud.update(self.db, user, **kwargs)

    def delete_user(self, user_id: int) -> Dict[str, str]:
        """
        删除用户

        Args:
            user_id: 用户ID

        Returns:
            删除结果
        """
        success = self.user_crud.delete(self.db, user_id)
        if not success:
            raise NotFoundException("用户", user_id)
        return {"message": "用户删除成功"}

    def assign_roles(
        self,
        user_id: int,
        role_ids: List[int]
    ) -> Dict[str, str]:
        """
        分配角色

        Args:
            user_id: 用户ID
            role_ids: 角色ID列表

        Returns:
            分配结果
        """
        success = self.user_crud.assign_roles(self.db, user_id, role_ids)
        if not success:
            raise NotFoundException("用户", user_id)
        return {"message": "角色分配成功"}

    def get_user_roles(self, user_id: int) -> List[Role]:
        """
        获取用户角色

        Args:
            user_id: 用户ID

        Returns:
            角色列表
        """
        user = self.user_crud.get_by_id(self.db, user_id)
        if not user:
            raise NotFoundException("用户", user_id)
        return user.roles

    def get_user_permissions(self, user_id: int) -> List[str]:
        """
        获取用户权限列表

        Args:
            user_id: 用户ID

        Returns:
            权限列表
        """
        user = self.user_crud.get_by_id(self.db, user_id)
        if not user:
            raise NotFoundException("用户", user_id)

        # 收集用户所有角色的权限
        permissions = set()
        for role in user.roles:
            for permission in role.permissions:
                permissions.add(f"{permission.resource}:{permission.action}")

        return list(permissions)


class UserService:
    """用户服务类"""

    def __init__(self, db: Session):
        """初始化用户服务"""
        self.db = db
        self.user_crud = UserCRUD()

    def create_user(
        self,
        username: str,
        password: str,
        phone: Optional[str] = None,
        email: Optional[str] = None,
        nickname: Optional[str] = None,
        gender: Optional[int] = None,
        avatar_url: Optional[str] = None
    ) -> User:
        """
        创建用户（管理员用）

        Args:
            username: 用户名
            password: 密码
            phone: 手机号
            email: 邮箱
            nickname: 昵称
            gender: 性别
            avatar_url: 头像URL

        Returns:
            用户对象
        """
        # 检查用户名是否已存在
        existing_user = self.user_crud.get_by_username(self.db, username)
        if existing_user:
            raise BadRequestException("用户名已存在")

        # 检查手机号是否已存在
        if phone:
            existing_phone = self.user_crud.get_by_phone(self.db, phone)
            if existing_phone:
                raise BadRequestException("手机号已被注册")

        # 检查邮箱是否已存在
        if email:
            existing_email = self.user_crud.get_by_email(self.db, email)
            if existing_email:
                raise BadRequestException("邮箱已被注册")

        # 创建用户
        return self.user_crud.create(
            db=self.db,
            username=username,
            password=password,
            phone=phone,
            email=email,
            nickname=nickname,
            gender=gender,
            avatar_url=avatar_url
        )

    def get_user(self, user_id: int) -> User:
        """
        获取用户详情

        Args:
            user_id: 用户ID

        Returns:
            用户对象
        """
        user = self.user_crud.get_by_id(self.db, user_id)
        if not user:
            raise NotFoundException("用户", user_id)
        return user

    def get_user_list(
        self,
        skip: int = 0,
        limit: int = 20,
        username: Optional[str] = None,
        phone: Optional[str] = None,
        email: Optional[str] = None,
        status: Optional[int] = None
    ) -> tuple[List[User], int]:
        """
        获取用户列表

        Args:
            skip: 跳过条数
            limit: 限制条数
            username: 用户名（模糊查询）
            phone: 手机号（模糊查询）
            email: 邮箱（模糊查询）
            status: 状态

        Returns:
            (用户列表, 总数)元组
        """
        return self.user_crud.get_list(
            db=self.db,
            skip=skip,
            limit=limit,
            username=username,
            phone=phone,
            email=email,
            status=status
        )

    def update_user(
        self,
        user_id: int,
        **kwargs
    ) -> User:
        """
        更新用户信息

        Args:
            user_id: 用户ID
            **kwargs: 更新的字段

        Returns:
            更新后的用户对象
        """
        user = self.user_crud.get_by_id(self.db, user_id)
        if not user:
            raise NotFoundException("用户", user_id)

        return self.user_crud.update(self.db, user, **kwargs)

    def delete_user(self, user_id: int) -> Dict[str, str]:
        """
        删除用户

        Args:
            user_id: 用户ID

        Returns:
            删除结果
        """
        success = self.user_crud.delete(self.db, user_id)
        if not success:
            raise NotFoundException("用户", user_id)
        return {"message": "用户删除成功"}

    def assign_roles(
        self,
        user_id: int,
        role_ids: List[int]
    ) -> Dict[str, str]:
        """
        分配角色

        Args:
            user_id: 用户ID
            role_ids: 角色ID列表

        Returns:
            分配结果
        """
        success = self.user_crud.assign_roles(self.db, user_id, role_ids)
        if not success:
            raise NotFoundException("用户", user_id)
        return {"message": "角色分配成功"}

    def get_user_roles(self, user_id: int) -> List[Role]:
        """
        获取用户角色

        Args:
            user_id: 用户:
            角色ID

        Returns列表
        """
        user = self.user_crud.get_by_id(self.db, user_id)
        if not user:
            raise NotFoundException("用户", user_id)
        return user.roles

    def get_user_permissions(self, user_id: int) -> List[str]:
        """
        获取用户权限列表

        Args:
            user_id: 用户ID

        Returns:
            权限列表
        """
        user = self.user_crud.get_by_id(self.db, user_id)
        if not user:
            raise NotFoundException("用户", user_id)

        # 收集用户所有角色的权限
        permissions = set()
        for role in user.roles:
            for permission in role.permissions:
                permissions.add(f"{permission.resource}:{permission.action}")

        return list(permissions)


class RoleService:
    """角色服务类"""

    def __init__(self, db: Session):
        """初始化角色服务"""
        self.db = db
        self.role_crud = RoleCRUD()

    def get_role(self, role_id: int) -> Role:
        """获取角色详情"""
        role = self.role_crud.get_by_id(self.db, role_id)
        if not role:
            raise NotFoundException("角色", role_id)
        return role

    def get_role_list(
        self,
        skip: int = 0,
        limit: int = 20,
        status: Optional[int] = None
    ) -> tuple[List[Role], int]:
        """获取角色列表"""
        return self.role_crud.get_list(
            db=self.db,
            skip=skip,
            limit=limit,
            status=status
        )

    def create_role(
        self,
        role_name: str,
        description: Optional[str] = None
    ) -> Role:
        """创建角色"""
        # 检查角色名是否已存在
        existing_role = self.role_crud.get_by_name(self.db, role_name)
        if existing_role:
            raise BadRequestException("角色名称已存在")

        return self.role_crud.create(
            db=self.db,
            role_name=role_name,
            description=description
        )

    def update_role(
        self,
        role_id: int,
        **kwargs
    ) -> Role:
        """更新角色"""
        role = self.role_crud.get_by_id(self.db, role_id)
        if not role:
            raise NotFoundException("角色", role_id)

        return self.role_crud.update(self.db, role, **kwargs)

    def delete_role(self, role_id: int) -> Dict[str, str]:
        """删除角色"""
        success = self.role_crud.delete(self.db, role_id)
        if not success:
            raise NotFoundException("角色", role_id)
        return {"message": "角色删除成功"}
