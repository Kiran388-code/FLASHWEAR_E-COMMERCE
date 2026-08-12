from fastapi import APIRouter
from app.schemas.rider import OTPVerificationRequest, RiderDeliveryUpdate
from app.services.rider import rider_service

router = APIRouter()

@router.get("/profile")
async def get_rider_profile(rider_id: int = 101):
    """Retrieve rider profile and active earnings."""
    return rider_service.get_rider_profile(rider_id)

@router.get("/assigned-orders")
async def get_assigned_orders(rider_id: int = 101):
    """Get active orders assigned to the rider."""
    return rider_service.get_assigned_orders(rider_id)

@router.post("/accept-order/{order_number}")
async def accept_order(order_number: str):
    """Rider accepts order assignment."""
    return rider_service.accept_order(order_number)

@router.post("/location")
async def update_location(update_in: RiderDeliveryUpdate):
    """Publish live GPS location update for customer tracking."""
    return rider_service.update_location(update_in.rider_id, update_in.current_lat, update_in.current_lng)

@router.post("/verify-otp")
async def verify_otp(verify_in: OTPVerificationRequest):
    """Verify customer OTP (e.g. 2587) at doorstep delivery."""
    return rider_service.verify_otp_and_complete(str(verify_in.order_id), verify_in.otp)
