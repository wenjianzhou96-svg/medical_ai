"""
医疗智能体系统 - Redis连接模块

提供Redis缓存连接和管理功能
"""

from typing import Optional, Any
import json
from redis import Redis, ConnectionPool
from app.core.config import settings
from app.core.logging import logger

# 创建Redis连接池
redis_pool = ConnectionPool.from_url(
    settings.redis_url,
    max_connections=50,
    decode_responses=True
)


def get_redis_client(db: int = 0) -> Redis:
    """
    获取Redis客户端
    
    Args:
        db: 数据库编号
    
    Returns:
        Redis: Redis客户端
    """
    return Redis(connection_pool=redis_pool, db=db)


class RedisCache:
    """Redis缓存类"""
    
    def __init__(self, db: int = 0):
        """
        初始化Redis缓存
        
        Args:
            db: 数据库编号
        """
        self.client = get_redis_client(db)
    
    def get(self, key: str) -> Optional[Any]:
        """
        获取缓存值
        
        Args:
            key: 缓存键
        
        Returns:
            Optional[Any]: 缓存值
        """
        try:
            value = self.client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.error(f"Redis get error: {e}")
            return None
    
    def set(self, key: str, value: Any, expire: int = 3600) -> bool:
        """
        设置缓存值
        
        Args:
            key: 缓存键
            value: 缓存值
            expire: 过期时间(秒)
        
        Returns:
            bool: 是否成功
        """
        try:
            self.client.setex(key, expire, json.dumps(value, ensure_ascii=False))
            return True
        except Exception as e:
            logger.error(f"Redis set error: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """
        删除缓存
        
        Args:
            key: 缓存键
        
        Returns:
            bool: 是否成功
        """
        try:
            self.client.delete(key)
            return True
        except Exception as e:
            logger.error(f"Redis delete error: {e}")
            return False
    
    def exists(self, key: str) -> bool:
        """
        检查缓存是否存在
        
        Args:
            key: 缓存键
        
        Returns:
            bool: 是否存在
        """
        try:
            return self.client.exists(key) > 0
        except Exception as e:
            logger.error(f"Redis exists error: {e}")
            return False
    
    def incr(self, key: str, amount: int = 1) -> int:
        """
        增加缓存值
        
        Args:
            key: 缓存键
            amount: 增加量
        
        Returns:
            int: 增加后的值
        """
        try:
            return self.client.incr(key, amount)
        except Exception as e:
            logger.error(f"Redis incr error: {e}")
            return 0
    
    def expire(self, key: str, expire: int) -> bool:
        """
        设置缓存过期时间
        
        Args:
            key: 缓存键
            expire: 过期时间(秒)
        
        Returns:
            bool: 是否成功
        """
        try:
            return self.client.expire(key, expire)
        except Exception as e:
            logger.error(f"Redis expire error: {e}")
            return False


# 创建默认缓存实例
cache = RedisCache(db=settings.redis_cache_db)
session_cache = RedisCache(db=settings.redis_session_db)
