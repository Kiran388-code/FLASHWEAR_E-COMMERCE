from fastapi import Request, status
from fastapi.responses import JSONResponse

class CustomAppException(Exception):
    """Base exception class for all custom application errors."""
    def __init__(self, detail: str, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR) -> None:
        self.detail = detail
        self.status_code = status_code
        super().__init__(detail)

class NotFoundException(CustomAppException):
    def __init__(self, detail: str = "Resource not found") -> None:
        super().__init__(detail, status.HTTP_404_NOT_FOUND)

class BadRequestException(CustomAppException):
    def __init__(self, detail: str = "Bad request") -> None:
        super().__init__(detail, status.HTTP_400_BAD_REQUEST)

class NotAuthenticatedException(CustomAppException):
    def __init__(self, detail: str = "Not authenticated") -> None:
        super().__init__(detail, status.HTTP_401_UNAUTHORIZED)

class ForbiddenException(CustomAppException):
    def __init__(self, detail: str = "Permission denied") -> None:
        super().__init__(detail, status.HTTP_403_FORBIDDEN)

async def app_exception_handler(request: Request, exc: CustomAppException) -> JSONResponse:
    """Global handler for application exceptions to return uniform JSON error payloads."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "message": exc.detail,
                "code": exc.__class__.__name__
            }
        }
    )
