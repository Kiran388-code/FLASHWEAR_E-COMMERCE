from typing import Dict, Any
from fastapi import APIRouter, Depends
from app.api.deps import get_current_user
from app.schemas.user import UserResponse

router = APIRouter()

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
    """Retrieve details of the currently logged-in user (from token)."""
    return current_user
