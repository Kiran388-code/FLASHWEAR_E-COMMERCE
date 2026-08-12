from app.repositories.base import BaseRepository
from app.repositories.user import user_repository, UserRepository
from app.repositories.product import product_repository, ProductRepository

__all__ = [
    "BaseRepository",
    "user_repository",
    "UserRepository",
    "product_repository",
    "ProductRepository",
]
