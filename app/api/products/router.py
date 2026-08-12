from typing import List, Optional
from fastapi import APIRouter

router = APIRouter()

# Empty product list - Products are added manually by Sellers via Seller Partner Portal or API
PRODUCTS_DATA = []

@router.get("/")
async def list_products(category: Optional[str] = None, search: Optional[str] = None, gender: Optional[str] = None):
    """Retrieve list of clothing products."""
    res = PRODUCTS_DATA
    if gender:
        res = [p for p in res if gender.lower() in p["gender"].lower() or p["gender"].lower() == "unisex"]
    if category:
        res = [p for p in res if category.lower() in p["category"].lower() or category.lower() in p["category"].lower().replace("'", "").replace(" ", "-")]
    if search:
        res = [p for p in res if search.lower() in p["title"].lower() or search.lower() in p["category"].lower() or search.lower() in p["gender"].lower()]
    return res

@router.get("/{product_id}")
async def get_product_by_id(product_id: int):
    """Retrieve product details."""
    for p in PRODUCTS_DATA:
        if p["id"] == product_id:
            return p
    if PRODUCTS_DATA:
        return PRODUCTS_DATA[0]
    return {}
