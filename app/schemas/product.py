from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field

class ProductBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=255)
    sku: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = None
    price: Decimal = Field(..., gt=Decimal("0.00"))
    stock: int = Field(0, ge=0)
    category_id: Optional[int] = None
    brand_id: Optional[int] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    sku: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None
    stock: Optional[int] = None
    category_id: Optional[int] = None
    brand_id: Optional[int] = None

class ProductResponse(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }
