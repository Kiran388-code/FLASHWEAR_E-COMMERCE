from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter()

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8)

@router.post("/reset-password")
async def reset_password(req: ResetPasswordRequest) -> dict:
    """Reset password using token sent in forgot-password flow."""
    # Placeholder for verifying reset token and updating password in DB
    return {"message": "Password reset completed successfully."}
