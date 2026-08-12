import os
import firebase_admin
from firebase_admin import credentials
from app.core.config import settings
from app.core.logging import logger

def initialize_firebase() -> None:
    """Initializes the Firebase Admin SDK app instance."""
    if not firebase_admin._apps:
        logger.info("Initializing Firebase Admin SDK...")
        cred_path = settings.FIREBASE_CREDENTIALS_PATH
        
        if cred_path and os.path.exists(cred_path):
            try:
                cred = credentials.Certificate(cred_path)
                firebase_admin.initialize_app(cred, {
                    "projectId": settings.FIREBASE_PROJECT_ID
                })
                logger.info("Firebase initialized successfully using service account.")
            except Exception as e:
                logger.error(f"Failed to initialize Firebase with service account: {e}")
        else:
            logger.warning(
                f"Firebase service account file not found at: {cred_path}. "
                "Attempting to initialize using Application Default Credentials (ADC) or mock."
            )
            try:
                firebase_admin.initialize_app(options={
                    "projectId": settings.FIREBASE_PROJECT_ID
                })
                logger.info("Firebase initialized successfully using ADC.")
            except Exception as e:
                logger.error(f"Failed to initialize Firebase with default credentials: {e}")
