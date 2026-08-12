from typing import Optional
import aio_pika
from app.core.config import settings
from app.core.logging import logger

class RabbitMQClient:
    def __init__(self) -> None:
        self.connection: Optional[aio_pika.RobustConnection] = None
        self.channel: Optional[aio_pika.RobustChannel] = None

    async def connect(self) -> None:
        logger.info("Connecting to RabbitMQ...")
        vhost = settings.RABBITMQ_VHOST
        # Format connection URL
        user = settings.RABBITMQ_USER
        password = settings.RABBITMQ_PASSWORD
        host = settings.RABBITMQ_HOST
        port = settings.RABBITMQ_PORT
        url = f"amqp://{user}:{password}@{host}:{port}/{vhost.lstrip('/')}"
        
        self.connection = await aio_pika.connect_robust(url)
        self.channel = await self.connection.channel()
        logger.info("RabbitMQ connected successfully.")

    async def disconnect(self) -> None:
        logger.info("Disconnecting from RabbitMQ...")
        if self.channel:
            await self.channel.close()
        if self.connection:
            await self.connection.close()

rabbitmq_client = RabbitMQClient()

async def get_rabbitmq_channel() -> aio_pika.RobustChannel:
    if rabbitmq_client.channel is None:
        await rabbitmq_client.connect()
    assert rabbitmq_client.channel is not None
    return rabbitmq_client.channel
