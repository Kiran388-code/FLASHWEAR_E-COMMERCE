import time
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.logging import logger

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to log basic details of every HTTP request."""
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        
        try:
            response = await call_next(request)
        except Exception as e:
            process_time = (time.time() - start_time) * 1000
            logger.error(
                f"Request Failed: {request.method} {request.url.path} - "
                f"Error: {str(e)} - Duration: {process_time:.2f}ms"
            )
            raise e
            
        process_time = (time.time() - start_time) * 1000
        logger.info(
            f"Request: {request.method} {request.url.path} - "
            f"Status: {response.status_code} - Duration: {process_time:.2f}ms"
        )
        
        # Add performance header
        response.headers["X-Process-Time-Ms"] = f"{process_time:.2f}"
        return response
