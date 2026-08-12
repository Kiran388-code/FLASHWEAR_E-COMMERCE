from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from app.schemas.order import OrderCreate, OrderStepUpdate
from app.services.order import order_service

router = APIRouter()

@router.get("/")
async def list_orders(user_id: int = Query(1, description="User ID")):
    """List all orders for a customer."""
    return order_service.list_orders(user_id=user_id)

@router.post("/", status_code=201)
async def create_order(order_in: OrderCreate, user_id: int = Query(1)):
    """Create a new FlashWear quick delivery order."""
    return order_service.create_order(user_id=user_id, order_in=order_in)

@router.get("/{order_number}")
async def get_order_by_number(order_number: str):
    """Fetch order details and current tracking status."""
    order = order_service.get_order(order_number)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.patch("/{order_number}/step")
async def update_order_step(order_number: str, update_in: OrderStepUpdate):
    """Progress order through the 12-step FlashWear quick commerce flow."""
    updated = order_service.update_order_step(order_number, update_in.step_number)
    if not updated:
        raise HTTPException(status_code=404, detail="Order not found")
    return updated
