from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import BaseRepository
from app.models.product import Product

class ProductRepository(BaseRepository[Product]):
    """Repository handling custom Product queries."""
    def __init__(self) -> None:
        super().__init__(Product)

    async def get_by_sku(self, db: AsyncSession, sku: str) -> Optional[Product]:
        """Fetch a product by its unique SKU identifier."""
        result = await db.execute(select(Product).filter(Product.sku == sku))
        return result.scalars().first()

product_repository = ProductRepository()
