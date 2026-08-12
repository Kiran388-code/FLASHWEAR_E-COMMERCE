from fastapi import APIRouter
from app.schemas.ai import TryOnRequest, SizeRecommendationRequest, VoiceSearchRequest, ChatbotRequest
from app.services.ai import ai_service

router = APIRouter()

@router.post("/virtual-try-on")
async def virtual_try_on(req: TryOnRequest):
    """Virtual Try-On AI endpoint."""
    return ai_service.virtual_try_on(req.product_id, req.user_image_base64)

@router.post("/size-recommendation")
async def size_recommendation(req: SizeRecommendationRequest):
    """AI Size Recommendation based on body measurements and fit preferences."""
    return ai_service.recommend_size(req.height_cm, req.weight_kg, req.fit_preference)

@router.post("/voice-search")
async def voice_search(req: VoiceSearchRequest):
    """AI Voice Search query processing."""
    return ai_service.voice_search(req.transcript)

@router.post("/chatbot")
async def chatbot(req: ChatbotRequest):
    """Fashion Assistant Chatbot endpoint."""
    return ai_service.chatbot(req.message)
