from fastapi import APIRouter

router = APIRouter()

BRANDS_DATA = [
    {"id": 1, "name": "Puma", "slug": "puma"},
    {"id": 2, "name": "Nike", "slug": "nike"},
    {"id": 3, "name": "Zara", "slug": "zara"},
    {"id": 4, "name": "H&M", "slug": "hm"},
    {"id": 5, "name": "Levi's", "slug": "levis"}
]

@router.get("/")
async def list_brands():
    """List available fashion brands."""
    return BRANDS_DATA
