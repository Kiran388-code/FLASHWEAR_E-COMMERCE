from typing import Optional, List
from pydantic import BaseModel

class CartItemCreate(BaseModel):
    product_id: int
    product_name: str
    size: Optional[str] = "M"
    color: Optional[str] = "Black"
    quantity: int = 1
    price: float
    image_url: Optional[str] = None

class CartItemResponse(CartItemCreate):
    id: int
    user_id: int
    model_config = {"from_attributes": True}

class CartSummary(BaseModel):
    items: List[CartItemResponse]
    subtotal: float
    discount: float
    total: float
