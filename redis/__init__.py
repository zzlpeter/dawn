"""
Redis连接池管理
"""
import aioredis

from tomlconfig import Config
from libs import singleton


__all__ = [
    'redis_pools'
]


@singleton
class Redis:
    redis_pools = {}

    def __init__(self):
        pass

    async def create_pools(self):
        _redis_pools = {}
        redis_conf = Config().redis
        for alias, cnf in redis_conf.items():
            address = cnf.pop('host')
            port = cnf.pop('port')
            conn = await aioredis.create_redis_pool((address, port), **cnf)
            _redis_pools[alias] = conn
        self.redis_pools = _redis_pools

    @property
    async def pools(self):
        if not self.redis_pools:
            await self.create_pools()
        return self.redis_pools


RedisPools = Redis().pools


async def redis_pools(alias):
    pools = await RedisPools
    return pools[alias]
