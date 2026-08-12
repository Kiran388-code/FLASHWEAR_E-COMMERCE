from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel

class OrderCreate(BaseModel):
    delivery_address: str
    payment_method: str = "UPI"
    cart_items: Optional[List[Dict[str, Any]]] = None

class OrderStepUpdate(BaseModel):
    step_number: int
    status: str

class OrderResponse(BaseModel):
    id: int
    order_number: str
    user_id: int
    status: str
    step_number: int
    total_amount: float
    items_summary: Dict[str, Any]
    delivery_address: str
    payment_method: str
    payment_status: str
    eta_minutes: int
    delivery_otp: str
    rider_name: Optional[str] = "Rahul Kumar"
    rider_phone: Optional[str] = "+91 9876543210"
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
