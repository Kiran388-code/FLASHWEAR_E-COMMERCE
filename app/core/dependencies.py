from typing import AsyncGenerator
import redis.asyncio as aioredis
from elasticsearch import AsyncElasticsearch
import aio_pika
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db as _get_db
from app.core.redis import get_redis as _get_redis
from app.core.rabbitmq import get_rabbitmq_channel as _get_rabbitmq
from app.core.elasticsearch import get_elasticsearch as _get_elasticsearch

# Re-export core async resources for FastAPI route dependency injection
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async for session in _get_db():
        yield session

async def get_redis_client() -> AsyncGenerator[aioredis.Redis, None]:
    async for client in _get_redis():
        yield client

async def get_rabbitmq_channel() -> aio_pika.RobustChannel:
    return await _get_rabbitmq()

async def get_elasticsearch_client() -> AsyncElasticsearch:
    return await _get_elasticsearch()
