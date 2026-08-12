from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_db_session
from app.schemas.user import UserCreate
from app.services.otp_service import otp_service

router = APIRouter()

@router.post("/register", status_code=200)
async def register(
    user_in: UserCreate, 
    db: AsyncSession = Depends(get_db_session)
) -> dict:
    """Dispatches a registration verification email link via SMTP."""
    res = await otp_service.send_registration_verification_email(db, user_in)
    if not res["success"]:
        raise HTTPException(status_code=400, detail=res["error"])
    return res
