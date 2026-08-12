from typing import Dict, Any, List, Optional

class AIService:
    def virtual_try_on(self, product_id: int, user_image_base64: Optional[str] = None) -> Dict[str, Any]:
        return {
            "product_id": product_id,
            "status": "success",
            "match_score": 98.4,
            "fit_analysis": "Excellent fit around shoulders and torso. Recommended size: M/L.",
            "render_url": "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=600&auto=format&fit=crop"
        }

    def recommend_size(self, height_cm: float, weight_kg: float, fit_preference: str = "regular") -> Dict[str, Any]:
        # BMI-based algorithm
        bmi = weight_kg / ((height_cm / 100) ** 2)
        if bmi < 18.5:
            rec_size = "S"
        elif bmi < 24.9:
            rec_size = "M" if fit_preference != "loose" else "L"
        elif bmi < 29.9:
            rec_size = "L" if fit_preference != "loose" else "XL"
        else:
            rec_size = "XL" if fit_preference != "loose" else "XXL"

        return {
            "height_cm": height_cm,
            "weight_kg": weight_kg,
            "fit_preference": fit_preference,
            "recommended_size": rec_size,
            "confidence": "96%",
            "fit_note": f"Based on your profile ({height_cm}cm, {weight_kg}kg), size {rec_size} gives you a comfortable {fit_preference} fit."
        }

    def voice_search(self, transcript: str) -> List[Dict[str, Any]]:
        return [
            {
                "id": 1,
                "title": "Men Solid Slim Fit Shirt",
                "price": 699.0,
                "category": "Western Wear",
                "delivery_mins": 15,
                "image": "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=400&auto=format&fit=crop"
            },
            {
                "id": 2,
                "title": "Blue Jeans Slim Fit",
                "price": 999.0,
                "category": "Jeans",
                "delivery_mins": 15,
                "image": "https://images.unsplash.com/photo-1542272604-780c36856842?w=400&auto=format&fit=crop"
            }
        ]

    def chatbot(self, message: str) -> Dict[str, Any]:
        msg_lower = message.lower()
        if "size" in msg_lower:
            reply = "I can help you find your exact size! Share your height and weight or try our AI Size Assistant."
        elif "delivery" in msg_lower or "track" in msg_lower or "order" in msg_lower:
            reply = "FlashWear delivers in 10-30 minutes! Your current order #FW123456 is on the way (ETA 3 mins)."
        elif "return" in msg_lower or "exchange" in msg_lower:
            reply = "We offer instant 10-minute doorstep exchanges and hassle-free returns."
        else:
            reply = f"Hi! I'm your FlashWear AI Assistant. I can assist with fashion choices, size recommendations, live tracking, and quick 15-minute delivery queries!"

        return {
            "reply": reply,
            "suggestions": ["Find my size", "Track my order #FW123456", "Recommended Outfits", "Flash Deals"]
        }

ai_service = AIService()
