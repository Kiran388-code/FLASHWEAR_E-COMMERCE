from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.product import product_repository
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate

class ProductService:
    """Service layer managing Product orchestration."""
    
    async def create_product(self, db: AsyncSession, product_in: ProductCreate) -> Product:
        """Create a new product."""
        return await product_repository.create(db, obj_in=product_in)

    async def get_product(self, db: AsyncSession, product_id: int) -> Optional[Product]:
        """Fetch a product by ID."""
        return await product_repository.get(db, id=product_id)

    async def list_products(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Product]:
        """List products with pagination."""
        return await product_repository.get_multi(db, skip=skip, limit=limit)

product_service = ProductService()
