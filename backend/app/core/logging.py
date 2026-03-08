"""
医疗智能体系统 - 日志配置模块

提供统一的日志配置和管理功能
"""

import logging
import os
from logging.handlers import RotatingFileHandler
from typing import Optional
from app.core.config import settings


def setup_logging(log_level: Optional[str] = None) -> logging.Logger:
    """
    配置日志系统
    
    Args:
        log_level: 日志级别
    
    Returns:
        logging.Logger: 配置好的日志器
    """
    # 创建logs目录
    log_dir = os.path.dirname(settings.log_file_path)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)
    
    # 获取根日志器
    logger = logging.getLogger()
    
    # 清除已有的处理器
    logger.handlers.clear()
    
    # 设置日志级别
    level = log_level or settings.log_level
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    
    # 日志格式
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # 文件处理器
    if settings.log_file_path:
        file_handler = RotatingFileHandler(
            filename=settings.log_file_path,
            maxBytes=settings.log_max_size,
            backupCount=settings.log_backup_count,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


# 创建默认日志器
logger = setup_logging()
