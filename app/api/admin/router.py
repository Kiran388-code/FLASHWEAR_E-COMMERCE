from fastapi import APIRouter

router = APIRouter()

@router.get("/dashboard")
async def get_admin_dashboard():
    """Retrieve system administrative overview."""
    return {
        "status": "operational",
        "warehouses": [
            {"id": 1, "name": "Koramangala Hub", "active_orders": 42, "status": "OPTIMAL"},
            {"id": 2, "name": "Indiranagar Hub", "active_orders": 38, "status": "OPTIMAL"}
        ],
        "system_health": {
            "api_gateway": "ONLINE",
            "message_queue": "HEALTHY",
            "redis_cache": "CONNECTED",
            "database": "HEALTHY"
        }
    }
