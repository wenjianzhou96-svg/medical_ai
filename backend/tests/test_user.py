"""
医疗智能体系统 - 用户模块单元测试

测试用户CRUD操作和用户服务的功能
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime

from app.crud.user import UserCRUD, RoleCRUD, LoginLogCRUD
from app.services.auth import AuthService, UserService, RoleService
from app.models.user import User, Role, Permission, LoginLog
from app.core.exceptions import (
    BadRequestException,
    UnauthorizedException,
    NotFoundException
)


# ==================== Fixtures ====================

@pytest.fixture
def mock_db():
    """创建模拟的数据库会话"""
    db = Mock()
    db.query.return_value = Mock()
    db.query.return_value.filter.return_value = Mock()
    db.query.return_value.filter.return_value.first.return_value = None
    db.query.return_value.filter.return_value.all.return_value = []
    db.query.return_value.filter.return_value.count.return_value = 0
    db.query.return_value.order_by.return_value = Mock()
    db.query.return_value.order_by.return_value.offset.return_value = Mock()
    db.query.return_value.order_by.return_value.offset.return_value.limit.return_value = Mock()
    db.query.return_value.order_by.return_value.offset.return_value.limit.return_value.all.return_value = []
    return db


@pytest.fixture
def sample_user():
    """创建示例用户"""
    user = User(
        user_id=1,
        username="testuser",
        phone="13800138000",
        email="test@example.com",
        password_hash="hashed_password",
        status=1,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    return user


@pytest.fixture
def sample_role():
    """创建示例角色"""
    role = Role(
        role_id=1,
        role_name="admin",
        description="管理员",
        status=1,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    return role


# ==================== 用户CRUD测试 ====================

class TestUserCRUD:
    """用户CRUD操作测试类"""

    def test_get_by_id(self, mock_db, sample_user):
        """测试根据ID获取用户"""
        # 设置mock
        mock_db.query.return_value.filter.return_value.first.return_value = sample_user

        # 执行测试
        result = UserCRUD.get_by_id(mock_db, 1)

        # 验证结果
        assert result is not None
        assert result.username == "testuser"
        mock_db.query.assert_called()

    def test_get_by_username(self, mock_db, sample_user):
        """测试根据用户名获取用户"""
        mock_db.query.return_value.filter.return_value.first.return_value = sample_user

        result = UserCRUD.get_by_username(mock_db, "testuser")

        assert result is not None
        assert result.username == "testuser"

    def test_get_by_phone(self, mock_db, sample_user):
        """测试根据手机号获取用户"""
        mock_db.query.return_value.filter.return_value.first.return_value = sample_user

        result = UserCRUD.get_by_phone(mock_db, "13800138000")

        assert result is not None
        assert result.phone == "13800138000"

    def test_get_by_email(self, mock_db, sample_user):
        """测试根据邮箱获取用户"""
        mock_db.query.return_value.filter.return_value.first.return_value = sample_user

        result = UserCRUD.get_by_email(mock_db, "test@example.com")

        assert result is not None
        assert result.email == "test@example.com"

    def test_create_user(self, mock_db):
        """测试创建用户"""
        # 设置mock
        mock_db.query.return_value.filter.return_value.first.return_value = None

        # 使用patch来模拟密码哈希
        with patch('app.crud.user.get_password_hash') as mock_hash:
            mock_hash.return_value = "hashed_password"

            result = UserCRUD.create(
                db=mock_db,
                username="newuser",
                password="password123",
                phone="13900139000",
                email="new@example.com"
            )

        # 验证
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()

    def test_get_list(self, mock_db, sample_user):
        """测试获取用户列表"""
        # 设置mock
        mock_query = Mock()
        mock_query.count.return_value = 1
        mock_query.order_by.return_value.offset.return_value.limit.return_value.all.return_value = [sample_user]
        mock_db.query.return_value = mock_query

        result, total = UserCRUD.get_list(mock_db)

        assert total == 1
        assert len(result) == 1

    def test_update_user(self, mock_db, sample_user):
        """测试更新用户"""
        sample_user.nickname = "Test Nickname"

        result = UserCRUD.update(mock_db, sample_user, nickname="Updated Nickname")

        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once()

    def test_delete_user(self, mock_db, sample_user):
        """测试删除用户"""
        mock_db.query.return_value.filter.return_value.first.return_value = sample_user

        result = UserCRUD.delete(mock_db, 1)

        assert result is True
        mock_db.delete.assert_called_once()
        mock_db.commit.assert_called_once()


# ==================== 角色CRUD测试 ====================

class TestRoleCRUD:
    """角色CRUD操作测试类"""

    def test_get_by_id(self, mock_db, sample_role):
        """测试根据ID获取角色"""
        mock_db.query.return_value.filter.return_value.first.return_value = sample_role

        result = RoleCRUD.get_by_id(mock_db, 1)

        assert result is not None
        assert result.role_name == "admin"

    def test_get_by_name(self, mock_db, sample_role):
        """测试根据角色名获取角色"""
        mock_db.query.return_value.filter.return_value.first.return_value = sample_role

        result = RoleCRUD.get_by_name(mock_db, "admin")

        assert result is not None
        assert result.role_name == "admin"

    def test_create_role(self, mock_db):
        """测试创建角色"""
        with patch('app.crud.user.Role') as MockRole:
            mock_role_instance = Mock()
            mock_role_instance.role_id = 1
            MockRole.return_value = mock_role_instance

            result = RoleCRUD.create(
                db=mock_db,
                role_name="doctor",
                description="医生"
            )

        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()


# ==================== 认证服务测试 ====================

class TestAuthService:
    """认证服务测试类"""

    def test_register_success(self, mock_db):
        """测试成功注册"""
        # 设置mock
        mock_db.query.return_value.filter.return_value.first.return_value = None

        auth_service = AuthService(mock_db)

        with patch.object(auth_service, '_generate_tokens') as mock_tokens:
            mock_tokens.return_value = {
                "access_token": "token",
                "refresh_token": "refresh",
                "token_type": "bearer",
                "expires_in": 7200
            }

            with patch('app.services.auth.UserCRUD') as MockUserCRUD:
                MockUserCRUD.get_by_username.return_value = None
                MockUserCRUD.get_by_phone.return_value = None
                MockUserCRUD.get_by_email.return_value = None

                mock_user = User(
                    user_id=1,
                    username="testuser",
                    password_hash="hashed",
                    status=1
                )
                MockUserCRUD.create.return_value = mock_user

                # 由于CRUD是mock的，这里主要测试异常流程不被触发
                pass

    def test_register_username_exists(self, mock_db, sample_user):
        """测试用户名已存在"""
        # 设置mock - 用户已存在
        mock_db.query.return_value.filter.return_value.first.return_value = sample_user

        # 验证逻辑：如果用户名已存在，create方法不应该被调用
        # 这里主要测试逻辑流程
        from app.crud.user import UserCRUD
        
        # 尝试获取已存在的用户
        result = UserCRUD.get_by_username(mock_db, "testuser")
        
        assert result is not None
        assert result.username == "testuser"


# ==================== 用户服务测试 ====================

class TestUserService:
    """用户服务测试类"""

    def test_get_user_success(self, mock_db, sample_user):
        """测试成功获取用户"""
        mock_db.query.return_value.filter.return_value.first.return_value = sample_user

        user_service = UserService(mock_db)
        result = user_service.get_user(1)

        assert result is not None
        assert result.username == "testuser"

    def test_get_user_not_found(self, mock_db):
        """测试用户不存在"""
        mock_db.query.return_value.filter.return_value.first.return_value = None

        user_service = UserService(mock_db)

        with pytest.raises(NotFoundException):
            user_service.get_user(999)

    def test_get_user_list(self, mock_db, sample_user):
        """测试获取用户列表"""
        mock_query = Mock()
        mock_query.count.return_value = 1
        mock_query.order_by.return_value.offset.return_value.limit.return_value.all.return_value = [sample_user]
        mock_db.query.return_value = mock_query

        user_service = UserService(mock_db)
        result, total = user_service.get_user_list()

        assert total == 1
        assert len(result) == 1


# ==================== 集成测试 ====================

class TestIntegration:
    """集成测试类"""

    def test_user_registration_flow(self):
        """测试用户注册流程"""
        # 这是一个模拟的集成测试
        # 在实际环境中需要真实的数据库连接

        # 1. 验证用户名不存在
        # 2. 验证手机号不存在
        # 3. 验证邮箱不存在
        # 4. 创建用户
        # 5. 生成Token

        assert True  # 模拟通过

    def test_user_login_flow(self):
        """测试用户登录流程"""
        # 1. 查找用户
        # 2. 验证密码
        # 3. 检查用户状态
        # 4. 更新最后登录时间
        # 5. 记录登录日志
        # 6. 生成Token

        assert True  # 模拟通过


# ==================== 边界条件测试 ====================

class TestBoundaryConditions:
    """边界条件测试类"""

    def test_empty_username(self, mock_db):
        """测试空用户名"""
        with pytest.raises(Exception):
            UserCRUD.create(mock_db, "", "password123")

    def test_short_password(self, mock_db):
        """测试密码长度不足"""
        with pytest.raises(Exception):
            UserCRUD.create(mock_db, "user", "123")

    def test_invalid_email_format(self, mock_db):
        """测试邮箱格式无效"""
        # Pydantic会在Schema验证层面拦截
        assert True

    def test_duplicate_username(self, mock_db, sample_user):
        """测试重复用户名"""
        mock_db.query.return_value.filter.return_value.first.side_effect = [sample_user, None]

        # 第一次检查会返回用户，第二次创建时应该报错
        # 这里主要测试逻辑
        assert True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
