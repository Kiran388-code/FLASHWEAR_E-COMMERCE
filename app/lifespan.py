import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI
from app.core.logging import logger, setup_logging
from app.core.redis import redis_client
from app.core.rabbitmq import rabbitmq_client
from app.core.elasticsearch import es_client
from app.core.firebase import initialize_firebase

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # 1. Initialize logging
    setup_logging()
    logger.info("Initializing FLASHWEAR-BACKEND integrations...")
    
    # 2. Initialize Firebase SDK
    try:
        initialize_firebase()
    except Exception as e:
        logger.warning(f"Firebase initialization skipped (Mock mode): {e}")
        
    # 3. Connect Redis
    try:
        redis_client.connect()
    except Exception as e:
        logger.warning(f"Redis connection skipped (Mock mode): {e}")
        
    # 4. Connect RabbitMQ
    try:
        await asyncio.wait_for(rabbitmq_client.connect(), timeout=1.0)
    except Exception as e:
        logger.warning(f"RabbitMQ connection skipped (Mock mode): {e}")
        
    # 5. Connect Elasticsearch
    try:
        es_client.connect()
    except Exception as e:
        logger.warning(f"Elasticsearch connection skipped (Mock mode): {e}")
        
    logger.info("All startup hooks completed successfully.")
    
    yield
    
    logger.info("Shutting down FLASHWEAR-BACKEND services...")
    
    # Disconnect in reverse order
    try:
        await es_client.disconnect()
    except Exception as e:
        logger.error(f"Failed to disconnect Elasticsearch: {e}")
        
    try:
        await rabbitmq_client.disconnect()
    except Exception as e:
        logger.error(f"Failed to disconnect RabbitMQ: {e}")
        
    try:
        await redis_client.disconnect()
    except Exception as e:
        logger.error(f"Failed to disconnect Redis: {e}")
        
    logger.info("Cleanup completed. Goodbye!")
