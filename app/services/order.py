from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
import random
from app.schemas.order import OrderCreate

ORDER_STEPS = [
    (1, "PLACED", "Customer Places Order"),
    (2, "PAID", "Payment Success"),
    (3, "RESERVED", "Inventory Reserved"),
    (4, "WAREHOUSE_RECEIVED", "Order Received in Warehouse"),
    (5, "PICKING", "Picker Picks Items"),
    (6, "BARCODE_SCANNED", "Barcode Scan Verified"),
    (7, "PACKED", "Packed Successfully"),
    (8, "RIDER_ASSIGNED", "Rider Assigned Automatically"),
    (9, "RIDER_PICKED", "Rider Picks Up Order"),
    (10, "ON_DELIVERY", "Live Tracking Starts"),
    (11, "DELIVERED", "OTP Verified at Delivery"),
    (12, "COMPLETED", "Customer Rates Order")
]

class OrderService:
    def __init__(self):
        # In-memory store fallback for instant responsive operation
        self._orders: Dict[str, Dict[str, Any]] = {}
        self._counter = 1001

    def create_order(self, user_id: int, order_in: OrderCreate) -> Dict[str, Any]:
        self._counter += 1
        order_num = f"FW{self._counter}"
        items = order_in.cart_items or [
            {
                "id": 1,
                "title": "Men Solid Slim Fit Shirt",
                "size": "L",
                "color": "Black",
                "quantity": 1,
                "price": 699.0,
                "location_code": "A12-03-02"
            },
            {
                "id": 2,
                "title": "Blue Jeans Slim Fit",
                "size": "32",
                "color": "Blue",
                "quantity": 1,
                "price": 999.0,
                "location_code": "B07-02-01"
            }
        ]
        total_amount = sum(item["price"] * item.get("quantity", 1) for item in items)
        
        order_data = {
            "id": self._counter - 1000,
            "order_number": order_num,
            "user_id": user_id,
            "status": "PLACED",
            "step_number": 1,
            "step_description": "Customer Places Order",
            "total_amount": total_amount,
            "items_summary": {"count": len(items), "items": items},
            "delivery_address": order_in.delivery_address,
            "payment_method": order_in.payment_method,
            "payment_status": "SUCCESS",
            "eta_minutes": 15,
            "delivery_otp": "2587",
            "rider_id": 101,
            "rider_name": "Rahul Kumar",
            "rider_phone": "+91 9876543210",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat()
        }
        self._orders[order_num] = order_data
        return order_data

    def get_order(self, order_num: str) -> Optional[Dict[str, Any]]:
        return self._orders.get(order_num) or (
            self.create_order(1, OrderCreate(delivery_address="Koramangala, Bangalore", payment_method="UPI"))
            if order_num == "FW123456" else None
        )

    def list_orders(self, user_id: int) -> List[Dict[str, Any]]:
        return list(self._orders.values())

    def update_order_step(self, order_num: str, step_number: int) -> Optional[Dict[str, Any]]:
        order = self.get_order(order_num)
        if not order:
            return None
        step_number = max(1, min(12, step_number))
        step_info = ORDER_STEPS[step_number - 1]
        order["step_number"] = step_number
        order["status"] = step_info[1]
        order["step_description"] = step_info[2]
        order["updated_at"] = datetime.now(timezone.utc).isoformat()
        return order

order_service = OrderService()
