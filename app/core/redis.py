from typing import AsyncGenerator, Optional
import redis.asyncio as aioredis
from app.core.config import settings
from app.core.logging import logger

class RedisClient:
    def __init__(self) -> None:
        self.client: Optional[aioredis.Redis] = None
        self.pool: Optional[aioredis.ConnectionPool] = None

    def connect(self) -> None:
        logger.info("Initializing Redis connection pool...")
        self.pool = aioredis.ConnectionPool(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASSWORD,
            db=settings.REDIS_DB,
            decode_responses=True
        )
        self.client = aioredis.Redis(connection_pool=self.pool)

    async def disconnect(self) -> None:
        if self.client:
            logger.info("Closing Redis connections...")
            await self.client.aclose()
        if self.pool:
            await self.pool.disconnect()

redis_client = RedisClient()

# Dependency provider
async def get_redis() -> AsyncGenerator[aioredis.Redis, None]:
    if redis_client.client is None:
        redis_client.connect()
    yield redis_client.client
