from typing import Dict, Any, List, Optional

class RiderService:
    def __init__(self):
        self._rider_info = {
            "id": 101,
            "name": "Rahul Kumar",
            "phone": "+91 9876543210",
            "current_lat": 12.9352,
            "current_lng": 77.6245,
            "is_available": True,
            "total_earnings": 45.00,
            "rating": 4.9
        }
        self._active_deliveries = {
            "FW123456": {
                "order_number": "FW123456",
                "customer_name": "Rahul Kumar",
                "delivery_address": "Koramangala, Bangalore",
                "pickup_address": "Indiranagar Warehouse Hub",
                "distance_km": 2.3,
                "earnings": 45.00,
                "otp": "2587",
                "status": "ACCEPTED", # ASSIGNED, ACCEPTED, PICKED_UP, DELIVERED
                "items_count": 3
            }
        }

    def get_rider_profile(self, rider_id: int) -> Dict[str, Any]:
        return self._rider_info

    def get_assigned_orders(self, rider_id: int) -> List[Dict[str, Any]]:
        return list(self._active_deliveries.values())

    def accept_order(self, order_number: str) -> Dict[str, Any]:
        delivery = self._active_deliveries.get(order_number)
        if delivery:
            delivery["status"] = "ACCEPTED"
        return {"status": "ACCEPTED", "message": "Order accepted by rider"}

    def update_location(self, rider_id: int, lat: float, lng: float) -> Dict[str, Any]:
        self._rider_info["current_lat"] = lat
        self._rider_info["current_lng"] = lng
        return {"success": True, "lat": lat, "lng": lng}

    def verify_otp_and_complete(self, order_number: str, otp: str) -> Dict[str, Any]:
        delivery = self._active_deliveries.get(order_number)
        expected_otp = delivery["otp"] if delivery else "2587"
        if otp == expected_otp:
            if delivery:
                delivery["status"] = "DELIVERED"
            self._rider_info["total_earnings"] += 45.00
            return {
                "verified": True,
                "order_number": order_number,
                "message": "OTP verified successfully. Order delivered!",
                "status": "DELIVERED"
            }
        return {"verified": False, "message": "Invalid OTP. Please check with customer."}

rider_service = RiderService()
