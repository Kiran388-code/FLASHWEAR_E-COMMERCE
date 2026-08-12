from typing import List, Optional
from decimal import Decimal
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field

router = APIRouter()

# In-Memory/Database Seller Store for fast access
SELLER_MOCK_DATA = {
    "store_name": "FlashWear Premium Hub",
    "business_email": "seller@flashwear.com",
    "phone": "+91 98765 43210",
    "rating": 4.9,
    "total_sales": 142800.0,
    "active_orders": 3,
    "total_products": 8
}

class SellerRegisterRequest(BaseModel):
    store_name: str = Field(..., min_length=3, description="Name of the seller store")
    business_email: str
    phone: str
    address: Optional[str] = "Koramangala 4th Block, Bengaluru"

class AddProductRequest(BaseModel):
    title: str = Field(..., min_length=3)
    description: str
    price: float = Field(..., gt=0)
    original_price: Optional[float] = None
    category: str
    gender: str = "Unisex"
    brand: str = "FlashWear Originals"
    stock: int = Field(default=20, ge=1)
    image_url: str

@router.get("/dashboard")
async def get_seller_dashboard():
    """Retrieve Seller analytics, sales counters, and active product metrics."""
    return {
        "success": True,
        "store": SELLER_MOCK_DATA["store_name"],
        "rating": SELLER_MOCK_DATA["rating"],
        "total_revenue": SELLER_MOCK_DATA["total_sales"],
        "total_products": SELLER_MOCK_DATA["total_products"],
        "active_orders": SELLER_MOCK_DATA["active_orders"],
        "message": "Seller dashboard analytics retrieved successfully."
    }

@router.post("/register")
async def register_seller(req: SellerRegisterRequest):
    """Registers a new third-party merchant store."""
    SELLER_MOCK_DATA["store_name"] = req.store_name
    SELLER_MOCK_DATA["business_email"] = req.business_email
    SELLER_MOCK_DATA["phone"] = req.phone
    return {
        "success": True,
        "store_name": req.store_name,
        "message": f"Merchant store '{req.store_name}' registered successfully!"
    }

@router.post("/products")
async def add_seller_product(req: AddProductRequest):
    """Allows sellers to host new clothing items on the FLASHWEAR platform."""
    from app.api.products.router import PRODUCTS_DATA
    
    new_id = len(PRODUCTS_DATA) + 1
    orig_price = req.original_price if req.original_price else float(round(req.price * 1.5, 2))
    discount = int(round(((orig_price - req.price) / orig_price) * 100)) if orig_price > req.price else 0
    
    new_product = {
        "id": new_id,
        "title": req.title,
        "description": req.description,
        "price": float(req.price),
        "original_price": float(orig_price),
        "discount_percent": discount,
        "rating": 5.0,
        "reviews_count": 1,
        "sizes": ["S", "M", "L", "XL"],
        "colors": ["Black", "Navy", "White"],
        "category": req.category,
        "gender": req.gender,
        "brand": req.brand,
        "delivery_mins": 15,
        "stock": req.stock,
        "image_url": req.image_url
    }
    
    PRODUCTS_DATA.insert(0, new_product)
    SELLER_MOCK_DATA["total_products"] += 1
    
    return {
        "success": True,
        "product": new_product,
        "message": f"Product '{req.title}' successfully hosted on FLASHWEAR!"
    }
