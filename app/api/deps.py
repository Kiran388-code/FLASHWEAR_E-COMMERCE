from typing import Dict, Any
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_db_session
from app.core.security import oauth2_scheme
from app.core.jwt import decode_token
from app.core.exceptions import NotAuthenticatedException

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db_session)
) -> Dict[str, Any]:
    """Dependency to retrieve the currently authenticated user from JWT payload."""
    payload = decode_token(token)
    if not payload or payload.get("type") != "access":
        raise NotAuthenticatedException("Invalid or expired access token")
        
    user_id = payload.get("sub")
    if not user_id:
        raise NotAuthenticatedException("Token format error: subject ('sub') is missing")
        
    # Return placeholder User mapping to simulate fetched user
    return {
        "id": user_id,
        "email": payload.get("email", "unknown@flashwear.com"),
        "role": payload.get("role", "user"),
        "is_active": True
    }

async def get_current_active_user(
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """Dependency to ensure the current authenticated user is active."""
    if not current_user.get("is_active", False):
        raise NotAuthenticatedException("Inactive user account")
    return current_user
