from typing import Optional, List, Dict, Any
from pydantic import BaseModel

class TryOnRequest(BaseModel):
    user_image_base64: Optional[str] = None
    product_id: int

class SizeRecommendationRequest(BaseModel):
    height_cm: float
    weight_kg: float
    fit_preference: str = "regular" # tight, regular, loose

class VoiceSearchRequest(BaseModel):
    transcript: str

class ImageSearchRequest(BaseModel):
    image_base64: str

class ChatbotRequest(BaseModel):
    message: str
    context: Optional[Dict[str, Any]] = None
