
from redis.asyncio import Redis

from app.config import settings


redis_client: Redis | None = None


async def connect_redis() -> None:
    global redis_client

    redis_client = Redis.from_url(
        settings.REDIS_URL,
        encoding="utf-8",
        decode_responses=True,
        health_check_interval=30,
    )

    await redis_client.ping()


async def close_redis() -> None:
    global redis_client

    if redis_client is not None:
        await redis_client.aclose()
        redis_client = None


async def get_redis() -> Redis:
    if redis_client is None:
        raise RuntimeError("Redis is not initialized")

    return redis_client
