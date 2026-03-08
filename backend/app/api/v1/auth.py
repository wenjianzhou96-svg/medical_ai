"""
医疗智能体系统 - 认证路由

提供用户注册、登录、令牌刷新等功能
"""

from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr, Field

from app.core.database import get_db
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    verify_token
)
from app.core.exceptions import UnauthorizedException, BadRequestException
from app.core.logging import logger
from app.models.user import User, LoginLog
from app.api.v1.deps import get_current_user
from app.core.redis import session_cache

router = APIRouter()

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


# ============ Schema 定义 ============

class RegisterRequest(BaseModel):
    """注册请求"""
    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    password: str = Field(..., min_length=6, max_length=100, description="密码")
    phone: Optional[str] = Field(None, description="手机号")
    email: Optional[EmailStr] = Field(None, description="邮箱")


class LoginRequest(BaseModel):
    """登录请求"""
    username: str = Field(..., description="用户名")
    password: str = Field(..., description="密码")
    login_type: str = Field("password", description="登录类型: password/sms")


class TokenResponse(BaseModel):
    """令牌响应"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class UserResponse(BaseModel):
    """用户响应"""
    user_id: int
    username: str
    phone: Optional[str] = None
    email: Optional[str] = None
    avatar_url: Optional[str] = None
    nickname: Optional[str] = None
    status: int

    class Config:
        from_attributes = True


class LoginResponse(BaseModel):
    """登录响应"""
    token: TokenResponse
    user: UserResponse


class SendCodeRequest(BaseModel):
    """发送验证码请求"""
    phone: Optional[str] = Field(None, description="手机号")
    email: Optional[str] = Field(None, description="邮箱")
    type: str = Field("reset_password", description="验证码类型: reset_password/register")


class VerifyCodeRequest(BaseModel):
    """验证验证码请求"""
    phone: Optional[str] = Field(None, description="手机号")
    email: Optional[str] = Field(None, description="邮箱")
    code: str = Field(..., description="验证码")


class ResetPasswordRequest(BaseModel):
    """重置密码请求"""
    phone: Optional[str] = Field(None, description="手机号")
    email: Optional[str] = Field(None, description="邮箱")
    code: str = Field(..., description="验证码")
    new_password: str = Field(..., min_length=6, max_length=100, description="新密码")


# ============ 路由 ============

@router.post("/register", response_model=LoginResponse, summary="用户注册")
async def register(request: RegisterRequest, db: Session = Depends(get_db)):
    """用户注册"""
    # 检查用户名是否已存在
    existing_user = db.query(User).filter(User.username == request.username).first()
    if existing_user:
        raise BadRequestException("用户名已存在")
    
    # 检查手机号是否已存在
    if request.phone:
        existing_phone = db.query(User).filter(User.phone == request.phone).first()
        if existing_phone:
            raise BadRequestException("手机号已被注册")
    
    # 检查邮箱是否已存在
    if request.email:
        existing_email = db.query(User).filter(User.email == request.email).first()
        if existing_email:
            raise BadRequestException("邮箱已被注册")
    
    # 创建用户
    user = User(
        username=request.username,
        password_hash=get_password_hash(request.password),
        phone=request.phone,
        email=request.email,
        status=1
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # 生成令牌
    access_token = create_access_token(data={"sub": str(user.user_id), "username": user.username})
    refresh_token = create_refresh_token(data={"sub": str(user.user_id)})
    
    return LoginResponse(
        token=TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=7200
        ),
        user=UserResponse.model_validate(user)
    )


@router.post("/login", response_model=LoginResponse, summary="用户登录")
async def login(
    request: LoginRequest,
    req: Request,
    db: Session = Depends(get_db)
):
    """用户登录"""
    # 获取客户端IP
    client_ip = req.client.host if req.client else None
    user = db.query(User).filter(User.username == request.username).first()
    if not user:
        raise UnauthorizedException("用户名或密码错误")
    
    # 验证密码
    if not verify_password(request.password, user.password_hash):
        # 记录登录失败日志
        login_log = LoginLog(
            user_id=user.user_id,
            login_type=request.login_type,
            login_status=0,
            failure_reason="密码错误",
            ip_address=client_ip
        )
        db.add(login_log)
        db.commit()
        raise UnauthorizedException("用户名或密码错误")
    
    # 检查用户状态
    if user.status != 1:
        raise UnauthorizedException("账户已被禁用")
    
    # 更新最后登录时间
    user.last_login_at = datetime.utcnow()
    db.commit()
    
    # 记录登录成功日志
    login_log = LoginLog(
        user_id=user.user_id,
        login_type=request.login_type,
        login_status=1,
        ip_address=client_ip
    )
    db.add(login_log)
    db.commit()
    
    # 生成令牌
    access_token = create_access_token(data={"sub": str(user.user_id), "username": user.username})
    refresh_token = create_refresh_token(data={"sub": str(user.user_id)})
    
    return LoginResponse(
        token=TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=7200
        ),
        user=UserResponse.model_validate(user)
    )


@router.post("/refresh-token", response_model=TokenResponse, summary="刷新令牌")
async def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    """刷新访问令牌"""
    # 验证刷新令牌
    payload = verify_token(refresh_token)
    if not payload:
        raise UnauthorizedException("无效的刷新令牌")
    
    # 获取用户
    user_id = payload.get("sub")
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user or user.status != 1:
        raise UnauthorizedException("用户不存在或已被禁用")
    
    # 生成新令牌
    new_access_token = create_access_token(data={"sub": str(user.user_id), "username": user.username})
    new_refresh_token = create_refresh_token(data={"sub": str(user.user_id)})
    
    return TokenResponse(
        access_token=new_access_token,
        refresh_token=new_refresh_token,
        expires_in=7200
    )


@router.post("/logout", summary="用户登出")
async def logout(current_user: User = Depends(get_current_user)):
    """用户登出"""
    # 在实际应用中，可能需要将令牌加入黑名单
    return {"message": "登出成功"}


@router.get("/me", response_model=UserResponse, summary="获取当前用户信息")
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """获取当前登录用户信息"""
    return UserResponse.model_validate(current_user)


@router.post("/send-code", summary="发送验证码")
async def send_verification_code(request: SendCodeRequest, db: Session = Depends(get_db)):
    """发送验证码到手机或邮箱"""
    # 检查手机号或邮箱是否至少提供一个
    if not request.phone and not request.email:
        raise BadRequestException("请提供手机号或邮箱")
    
    # 验证手机号或邮箱是否已注册
    if request.phone:
        existing_user = db.query(User).filter(User.phone == request.phone).first()
        if not existing_user:
            raise BadRequestException("该手机号未注册")
        # 生成验证码
        import random
        code = str(random.randint(100000, 999999))
        # 存储验证码到Redis
        session_cache.set(f"verify_code:phone:{request.phone}", code, expire=300)  # 5分钟有效期
        # TODO: 调用短信服务发送验证码
        logger.info(f"验证码已发送(模拟): 手机号 {request.phone}, 验证码 {code}")
        return {"message": "验证码已发送", "phone": request.phone[-4:].rjust(11, '*')}
    
    if request.email:
        existing_user = db.query(User).filter(User.email == request.email).first()
        if not existing_user:
            raise BadRequestException("该邮箱未注册")
        # 生成验证码
        import random
        code = str(random.randint(100000, 999999))
        # 存储验证码到Redis
        session_cache.set(f"verify_code:email:{request.email}", code, expire=300)  # 5分钟有效期
        # TODO: 调用邮件服务发送验证码
        logger.info(f"验证码已发送(模拟): 邮箱 {request.email}, 验证码 {code}")
        return {"message": "验证码已发送", "email": request.email[:2] + '***' + request.email.split('@')[-1]}


@router.post("/verify-code", summary="验证验证码")
async def verify_code(request: VerifyCodeRequest):
    """验证验证码是否正确"""
    if not request.phone and not request.email:
        raise BadRequestException("请提供手机号或邮箱")
    
    if request.phone:
        stored_code = session_cache.get(f"verify_code:phone:{request.phone}")
        if not stored_code:
            raise BadRequestException("验证码已过期，请重新发送")
        if stored_code != request.code:
            raise BadRequestException("验证码错误")
        # 验证成功后删除验证码
        session_cache.delete(f"verify_code:phone:{request.phone}")
        return {"message": "验证成功"}
    
    if request.email:
        stored_code = session_cache.get(f"verify_code:email:{request.email}")
        if not stored_code:
            raise BadRequestException("验证码已过期，请重新发送")
        if stored_code != request.code:
            raise BadRequestException("验证码错误")
        # 验证成功后删除验证码
        session_cache.delete(f"verify_code:email:{request.email}")
        return {"message": "验证成功"}


@router.post("/reset-password", summary="重置密码")
async def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    """重置用户密码"""
    if not request.phone and not request.email:
        raise BadRequestException("请提供手机号或邮箱")
    
    # 验证验证码
    if request.phone:
        stored_code = session_cache.get(f"verify_code:phone:{request.phone}")
        if not stored_code:
            raise BadRequestException("验证码已过期，请重新发送")
        if stored_code != request.code:
            raise BadRequestException("验证码错误")
        # 获取用户
        user = db.query(User).filter(User.phone == request.phone).first()
    else:
        stored_code = session_cache.get(f"verify_code:email:{request.email}")
        if not stored_code:
            raise BadRequestException("验证码已过期，请重新发送")
        if stored_code != request.code:
            raise BadRequestException("验证码错误")
        # 获取用户
        user = db.query(User).filter(User.email == request.email).first()
    
    if not user:
        raise BadRequestException("用户不存在")
    
    # 更新密码
    user.password_hash = get_password_hash(request.new_password)
    db.commit()
    
    # 删除验证码
    if request.phone:
        session_cache.delete(f"verify_code:phone:{request.phone}")
    else:
        session_cache.delete(f"verify_code:email:{request.email}")
    
    return {"message": "密码重置成功，请使用新密码登录"}


class ChangePasswordRequest(BaseModel):
    """修改密码请求"""
    old_password: str = Field(..., description="原密码")
    new_password: str = Field(..., min_length=6, max_length=100, description="新密码")


@router.post("/change-password", summary="修改密码")
async def change_password(
    request: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """修改当前用户密码"""
    # 验证旧密码
    if not verify_password(request.old_password, current_user.password_hash):
        raise BadRequestException("原密码错误")

    # 更新密码
    current_user.password_hash = get_password_hash(request.new_password)
    db.commit()

    return {"message": "密码修改成功"}
