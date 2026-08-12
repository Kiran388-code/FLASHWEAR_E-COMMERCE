from fastapi import APIRouter

router = APIRouter()

@router.get("/overview")
async def get_analytics_overview():
    """Retrieve high-level quick commerce sales and performance metrics."""
    return {
        "today_orders": 1420,
        "avg_delivery_time_mins": 14.2,
        "total_revenue_inr": 284500.0,
        "active_riders": 85,
        "on_time_delivery_rate": "98.6%",
        "top_categories": [
            {"category": "Western Wear", "sales": 450},
            {"category": "Footwear", "sales": 380},
            {"category": "Ethnic Wear", "sales": 290}
        ]
    }
