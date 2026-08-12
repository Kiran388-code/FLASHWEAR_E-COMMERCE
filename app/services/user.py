from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user import user_repository
from app.schemas.user import UserCreate, UserLogin, Token
from app.core.hashing import hash_password, verify_password
from app.core.jwt import create_access_token, create_refresh_token
from app.core.exceptions import BadRequestException, NotAuthenticatedException
from app.models.user import User

class UserService:
    """Service layer managing User and Auth orchestration."""
    
    async def register(self, db: AsyncSession, user_in: UserCreate) -> User:
        """Register a new user, hashing their password in the process."""
        existing_user = await user_repository.get_by_email(db, user_in.email)
        if existing_user:
            raise BadRequestException("Email is already registered.")
            
        user_data = user_in.model_dump()
        raw_password = user_data.pop("password")
        user_data["hashed_password"] = hash_password(raw_password)
        
        return await user_repository.create(db, obj_in=user_data)

    async def authenticate(self, db: AsyncSession, login_in: UserLogin) -> Token:
        """Authenticate user email/password, returning access & refresh tokens."""
        user = await user_repository.get_by_email(db, login_in.email)
        if not user:
            raise NotAuthenticatedException("You are not registered. Please create an account first.")
        if not verify_password(login_in.password, user.hashed_password):
            raise NotAuthenticatedException("Incorrect password. Please check your password and try again.")
            
        if not user.is_active:
            raise BadRequestException("Inactive user profile.")
            
        # Create token payloads
        data = {"sub": str(user.id), "email": user.email, "role": user.role}
        
        access_token = create_access_token(data)
        refresh_token = create_refresh_token(data)
        
        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer"
        )

user_service = UserService()
