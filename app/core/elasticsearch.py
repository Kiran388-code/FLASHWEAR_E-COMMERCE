from typing import Optional
from elasticsearch import AsyncElasticsearch
from app.core.config import settings
from app.core.logging import logger

class ElasticsearchClient:
    def __init__(self) -> None:
        self.client: Optional[AsyncElasticsearch] = None

    def connect(self) -> None:
        logger.info("Initializing Elasticsearch connection...")
        hosts = [h.strip() for h in settings.ELASTICSEARCH_HOSTS.split(",")]
        
        # Configure auth if user and pass are provided
        kwargs = {}
        if settings.ELASTICSEARCH_USER and settings.ELASTICSEARCH_PASSWORD:
            kwargs["basic_auth"] = (settings.ELASTICSEARCH_USER, settings.ELASTICSEARCH_PASSWORD)
            
        self.client = AsyncElasticsearch(hosts, **kwargs)

    async def disconnect(self) -> None:
        if self.client:
            logger.info("Closing Elasticsearch connection...")
            await self.client.close()

es_client = ElasticsearchClient()

async def get_elasticsearch() -> AsyncElasticsearch:
    if es_client.client is None:
        es_client.connect()
    assert es_client.client is not None
    return es_client.client
