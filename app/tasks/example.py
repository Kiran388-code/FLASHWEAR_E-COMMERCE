import time
from app.workers.celery_app import celery_app
from app.core.logging import logger

@celery_app.task(name="send_notification_task")
def send_notification_task(email: str, content: str) -> bool:
    """Sample Celery background task simulating email notification dispatch."""
    logger.info(f"Task started: Sending notification to {email}...")
    time.sleep(2)  # Simulate latency
    logger.info(f"Task finished: Notification sent to {email}. Content length: {len(content)}")
    return True
