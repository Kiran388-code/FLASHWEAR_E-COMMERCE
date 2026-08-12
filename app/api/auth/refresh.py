from fastapi import APIRouter, Depends
from app.schemas.user import Token
from app.core.security import oauth2_scheme
from app.core.jwt import decode_token, create_access_token, create_refresh_token
from app.core.exceptions import NotAuthenticatedException

router = APIRouter()

@router.post("/refresh", response_model=Token)
async def refresh(token: str = Depends(oauth2_scheme)) -> Token:
    """Validate refresh token and issue a new access token & refresh token pair."""
    payload = decode_token(token)
    if not payload or payload.get("type") != "refresh":
        raise NotAuthenticatedException("Invalid or expired refresh token.")
        
    sub = payload.get("sub")
    email = payload.get("email")
    role = payload.get("role")
    
    new_payload = {"sub": sub, "email": email, "role": role}
    return Token(
        access_token=create_access_token(new_payload),
        refresh_token=create_refresh_token(new_payload),
        token_type="bearer"
    )
