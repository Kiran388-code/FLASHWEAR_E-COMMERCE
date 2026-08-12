from celery import Celery
from app.core.config import settings

# Initialize Celery app
celery_app = Celery(
    "flashwear_workers",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

# Optional configuration updates
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    # Auto-discover tasks from the tasks directory
    imports=["app.tasks.example"]
)
