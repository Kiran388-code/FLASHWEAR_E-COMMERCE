from typing import Optional
from pydantic import BaseModel

class RiderDeliveryUpdate(BaseModel):
    rider_id: int
    current_lat: float
    current_lng: float

class OTPVerificationRequest(BaseModel):
    order_id: int
    otp: str

class RiderResponse(BaseModel):
    id: int
    name: str
    phone: str
    current_lat: float
    current_lng: float
    is_available: bool
    total_earnings: float
    rating: float

    model_config = {"from_attributes": True}
