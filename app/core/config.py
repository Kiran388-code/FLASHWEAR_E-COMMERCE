from typing import Optional
from urllib.parse import quote_plus
from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )
    
    # App Settings
    APP_NAME: str = "FLASHWEAR-BACKEND"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    PORT: int = 8000
    HOST: str = "0.0.0.0"
    
    # PostgreSQL Database Settings
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "Flash@wear15"
    POSTGRES_HOST: str = "db.tqhxicrjcbnkcwdwykly.supabase.co"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "postgres"
    DATABASE_URL: Optional[str] = None
    
    @model_validator(mode="after")
    def assemble_db_connection(self) -> "Settings":
        if not self.DATABASE_URL:
            pwd = quote_plus(self.POSTGRES_PASSWORD)
            self.DATABASE_URL = f"postgresql+asyncpg://{self.POSTGRES_USER}:{pwd}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        elif self.DATABASE_URL.startswith("postgresql://"):
            self.DATABASE_URL = self.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
            
        # Enable SMTP automatically if user and password are provided
        if self.SMTP_USER and self.SMTP_PASSWORD and not self.SMTP_ENABLED:
            self.SMTP_ENABLED = True
            
        return self

    # SMTP Email Settings
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SMTP_FROM_EMAIL: str = "noreply@flashwear.com"
    SMTP_FROM_NAME: str = "FLASHWEAR Quick Commerce"
    SMTP_TLS: bool = True
    SMTP_SSL: bool = False
    SMTP_ENABLED: bool = False

    # Redis Settings
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: Optional[str] = None
    REDIS_DB: int = 0
    
    # RabbitMQ Settings
    RABBITMQ_HOST: str = "localhost"
    RABBITMQ_PORT: int = 5672
    RABBITMQ_USER: str = "guest"
    RABBITMQ_PASSWORD: str = "guest"
    RABBITMQ_VHOST: str = "/"
    
    # Celery Settings
    CELERY_BROKER_URL: str = "amqp://guest:guest@localhost:5672//"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"
    
    # Elasticsearch Settings
    ELASTICSEARCH_HOSTS: str = "http://localhost:9200"
    ELASTICSEARCH_USER: Optional[str] = None
    ELASTICSEARCH_PASSWORD: Optional[str] = None
    
    # Firebase Settings
    FIREBASE_PROJECT_ID: str = "flashwear-firebase-dev"
    FIREBASE_CREDENTIALS_PATH: Optional[str] = "secrets/firebase-service-account.json"
    
    # Security / JWT Settings
    JWT_SECRET_KEY: str = "supersecretkeythatisatleast32characterslongforjwtsecurity"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

settings = Settings()
