from typing import List, Optional, Dict, Any
from fastapi import APIRouter
from app.schemas.cart import CartItemCreate

router = APIRouter()

# In-memory cart store (Starts 100% EMPTY until customer adds items)
_cart_db: List[Dict[str, Any]] = []

@router.get("/")
async def get_cart():
    """Get active customer cart items and summary."""
    subtotal = sum(item["price"] * item["quantity"] for item in _cart_db)
    return {
        "items": _cart_db,
        "subtotal": subtotal,
        "discount": 0.0,
        "total": subtotal
    }

@router.post("/items", status_code=201)
async def add_item_to_cart(item_in: CartItemCreate):
    """Add a product item to customer cart."""
    new_item = {
        "id": len(_cart_db) + 1,
        "user_id": 1,
        "product_id": item_in.product_id,
        "product_name": item_in.product_name,
        "size": item_in.size,
        "color": item_in.color,
        "quantity": item_in.quantity,
        "price": item_in.price,
        "image_url": item_in.image_url or "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=400&auto=format&fit=crop"
    }
    _cart_db.append(new_item)
    return new_item

@router.delete("/items/{item_id}")
async def remove_item_from_cart(item_id: int):
    """Remove item from cart."""
    global _cart_db
    _cart_db = [item for item in _cart_db if item["id"] != item_id]
    return {"message": f"Item {item_id} removed from cart"}

@router.delete("/clear")
async def clear_cart():
    """Clear all items in cart."""
    global _cart_db
    _cart_db = []
    return {"message": "Cart cleared"}
