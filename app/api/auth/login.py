from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_db_session
from app.schemas.user import UserLogin, Token
from app.services.user import user_service

router = APIRouter()

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db_session)
) -> Token:
    """Login flow returning JWT access & refresh tokens."""
    login_in = UserLogin(email=form_data.username, password=form_data.password)
    return await user_service.authenticate(db, login_in)

@router.post("/login-json", response_model=Token)
async def login_json(
    login_in: UserLogin,
    db: AsyncSession = Depends(get_db_session)
) -> Token:
    """Alternative JSON-body login endpoint."""
    return await user_service.authenticate(db, login_in)
