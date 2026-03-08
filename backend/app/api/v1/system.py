"""
医疗智能体系统 - 系统路由
"""

from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.core.database import get_db
from app.models.system import SystemConfig

router = APIRouter()


class ConfigResponse(BaseModel):
    """配置响应"""
    config_id: int
    config_key: str
    config_value: str | None = None
    config_type: str
    description: str | None = None

    class Config:
        from_attributes = True


@router.get("/config", response_model=List[ConfigResponse], summary="获取系统配置")
async def get_configs(
    config_type: str | None = None,
    db: Session = Depends(get_db)
):
    """获取系统配置列表"""
    query = db.query(SystemConfig)
    if config_type:
        query = query.filter(SystemConfig.config_type == config_type)
    configs = query.all()
    return [ConfigResponse.model_validate(c) for c in configs]


@router.get("/config/{config_key}", response_model=ConfigResponse, summary="获取单个配置")
async def get_config(config_key: str, db: Session = Depends(get_db)):
    """获取指定配置"""
    config = db.query(SystemConfig).filter(SystemConfig.config_key == config_key).first()
    if not config:
        from app.core.exceptions import NotFoundException
        raise NotFoundException("配置", config_key)
    return ConfigResponse.model_validate(config)
