from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import BaseRepository
from app.models.user import User

class UserRepository(BaseRepository[User]):
    """Repository handling custom User queries."""
    def __init__(self) -> None:
        super().__init__(User)

    async def get_by_email(self, db: AsyncSession, email: str) -> Optional[User]:
        """Fetch a user by their email address."""
        result = await db.execute(select(User).filter(User.email == email))
        return result.scalars().first()

user_repository = UserRepository()
