from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class ReviewCreate(BaseModel):
    product_id: int
    rating: float
    comment: str

@router.get("/{product_id}")
async def get_reviews(product_id: int):
    return {
        "product_id": product_id,
        "average_rating": 4.6,
        "total_reviews": 128,
        "reviews": [
            {"user": "Rahul M.", "rating": 5.0, "comment": "Delivered in 12 mins! Amazing quality and exact fit."},
            {"user": "Priya S.", "rating": 4.5, "comment": "Great fabric and super fast delivery."}
        ]
    }

@router.post("/")
async def add_review(review: ReviewCreate):
    return {"status": "SUCCESS", "message": "Review submitted successfully!"}
