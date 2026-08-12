from typing import List
from fastapi import APIRouter

router = APIRouter()

CATEGORIES_DATA = [
    {"id": 1, "name": "Men's Western Wear", "slug": "mens-western", "image_url": "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=300&auto=format&fit=crop"},
    {"id": 2, "name": "Women's Dresses & Tops", "slug": "womens-western", "image_url": "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=300&auto=format&fit=crop"},
    {"id": 3, "name": "Men's Ethnic Wear", "slug": "mens-ethnic", "image_url": "https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=300&auto=format&fit=crop"},
    {"id": 4, "name": "Women's Ethnic & Sarees", "slug": "womens-ethnic", "image_url": "https://images.unsplash.com/photo-1617627143750-d86bc21e42bb?w=300&auto=format&fit=crop"},
    {"id": 5, "name": "Unisex Hoodies & Jackets", "slug": "unisex-casuals", "image_url": "https://images.unsplash.com/photo-1556905055-8f358a7a47b2?w=300&auto=format&fit=crop"}
]

@router.get("/")
async def list_categories():
    """List clothing categories for Men & Women."""
    return CATEGORIES_DATA
