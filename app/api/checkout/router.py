from fastapi import APIRouter
from app.schemas.order import OrderCreate
from app.services.order import order_service

router = APIRouter()

@router.post("/process")
async def process_checkout(order_in: OrderCreate):
    """Process checkout, reserve inventory, initiate payment, and return order confirmation."""
    created = order_service.create_order(user_id=1, order_in=order_in)
    return {
        "status": "SUCCESS",
        "order": created,
        "message": "Payment successful! 15-minute quick delivery sequence initiated."
    }
