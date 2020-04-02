import asyncio
from redis import redis_pools


async def main():
    redis = await redis_pools('default')

    await redis.hmset_dict('hash1',
                           key1='value1',
                           key2='value2',
                           key3=123)

    result = await redis.hgetall('hash', encoding='utf-8')
    # assert result == {
    #     'key1': 'value1',
    #     'key2': 'value2',
    #     'key3': '123',  # note that Redis returns int as string
    # }

    redis.close()
    await redis.wait_closed()

asyncio.run(main())