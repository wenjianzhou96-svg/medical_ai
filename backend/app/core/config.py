"""
医疗智能体系统 - 核心配置模块

提供应用配置管理、环境变量加载、安全工具等功能
"""

import os
from typing import List, Optional
from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """应用配置类"""

    # ==================== 应用配置 ====================
    app_name: str = Field(default="医疗智能体系统", description="应用名称")
    app_version: str = Field(default="1.0.0", description="应用版本")
    app_description: str = Field(default="基于大语言模型的医疗智能体系统", description="应用描述")
    debug: bool = Field(default=True, description="调试模式")
    secret_key: str = Field(default="your-secret-key-change-in-production", description="密钥")

    # ==================== 服务器配置 ====================
    host: str = Field(default="0.0.0.0", description="服务器主机")
    port: int = Field(default=8000, description="服务器端口")

    # ==================== 数据库配置 ====================
    database_url: str = Field(default="mysql+pymysql://root:password@localhost:3306/medical_ai", description="数据库连接URL")
    database_echo: bool = Field(default=False, description="是否打印SQL语句")
    db_pool_size: int = Field(default=10, description="数据库连接池大小")
    db_max_overflow: int = Field(default=20, description="数据库连接池最大溢出数")

    # ==================== Redis配置 ====================
    redis_url: str = Field(default="redis://localhost:6379/0", description="Redis连接URL")
    redis_cache_db: int = Field(default=1, description="Redis缓存数据库编号")
    redis_session_db: int = Field(default=2, description="Redis会话数据库编号")

    # ==================== 向量数据库配置 ====================
    vector_db_type: str = Field(default="chroma", description="向量数据库类型: chroma/pinecone/qdrant")
    chroma_persist_dir: str = Field(default="./data/chroma_db", description="Chroma数据持久化目录")

    # ==================== JWT配置 ====================
    jwt_secret_key: str = Field(default="your-jwt-secret-key-change-in-production", description="JWT密钥")
    jwt_algorithm: str = Field(default="HS256", description="JWT算法")
    access_token_expire_minutes: int = Field(default=120, description="访问令牌过期时间(分钟)")
    refresh_token_expire_days: int = Field(default=7, description="刷新令牌过期时间(天)")

    # ==================== 大语言模型配置 ====================
    qianwen_api_key: str = Field(default="", description="通义千问API Key")
    qianwen_model: str = Field(default="qwen-turbo", description="通义千问模型")
    qianwen_base_url: str = Field(default="https://dashscope.aliyuncs.com/compatible-mode/v1", description="通义千问API地址")

    openai_api_key: str = Field(default="", description="OpenAI API Key")
    openai_model: str = Field(default="gpt-3.5-turbo", description="OpenAI模型")
    openai_base_url: str = Field(default="https://api.openai.com/v1", description="OpenAI API地址")

    # ==================== 短信服务配置 ====================
    sms_provider: str = Field(default="aliyun", description="短信服务商")
    sms_access_key: str = Field(default="", description="短信Access Key")
    sms_secret_key: str = Field(default="", description="短信Secret Key")
    sms_sign_name: str = Field(default="医疗智能体", description="短信签名")
    sms_template_code: str = Field(default="", description="短信模板码")

    # ==================== 邮件服务配置 ====================
    smtp_host: str = Field(default="", description="SMTP主机")
    smtp_port: int = Field(default=587, description="SMTP端口")
    smtp_user: str = Field(default="", description="SMTP用户名")
    smtp_password: str = Field(default="", description="SMTP密码")
    smtp_from: str = Field(default="", description="发件人邮箱")

    # ==================== 文件存储配置 ====================
    storage_type: str = Field(default="local", description="存储类型: local/oss/cos")
    storage_local_path: str = Field(default="./uploads", description="本地存储路径")
    storage_oss_bucket: str = Field(default="", description="OSS存储桶")
    storage_oss_endpoint: str = Field(default="", description="OSS终端节点")

    # ==================== CORS配置 ====================
    cors_origins: str = Field(default="http://localhost:3000,http://localhost:5173", description="允许的跨域来源")

    # ==================== 日志配置 ====================
    log_level: str = Field(default="INFO", description="日志级别")
    log_file_path: str = Field(default="./logs/app.log", description="日志文件路径")
    log_max_size: int = Field(default=10485760, description="日志文件最大大小")
    log_backup_count: int = Field(default=5, description="日志文件保留数量")

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
        "extra": "ignore"
    }

    @property
    def cors_origins_list(self) -> List[str]:
        """获取CORS origins列表"""
        return [origin.strip() for origin in self.cors_origins.split(",")]

    @property
    def is_production(self) -> bool:
        """是否生产环境"""
        return not self.debug


@lru_cache()
def get_settings() -> Settings:
    """获取配置单例"""
    return Settings()


# 创建全局配置实例
settings = get_settings()
