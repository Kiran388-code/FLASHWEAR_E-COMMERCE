from app.services.user import user_service, UserService
from app.services.product import product_service, ProductService
from app.services.order import order_service, OrderService
from app.services.rider import rider_service, RiderService
from app.services.ai import ai_service, AIService

__all__ = [
    "user_service", "UserService",
    "product_service", "ProductService",
    "order_service", "OrderService",
    "rider_service", "RiderService",
    "ai_service", "AIService"
]
