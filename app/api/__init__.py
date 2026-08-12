from fastapi import APIRouter
from app.api.auth import auth_router
from app.api.users.router import router as users_router
from app.api.category.router import router as category_router
from app.api.brand.router import router as brand_router
from app.api.products.router import router as products_router
from app.api.cart.router import router as cart_router
from app.api.checkout.router import router as checkout_router
from app.api.orders.router import router as orders_router
from app.api.rider.router import router as rider_router
from app.api.seller.router import router as seller_router
from app.api.review.router import router as review_router
from app.api.notification.router import router as notification_router
from app.api.analytics.router import router as analytics_router
from app.api.admin.router import router as admin_router
from app.api.ai.router import router as ai_router

api_router = APIRouter()

# Register all sub-routers
api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users_router, prefix="/users", tags=["Users"])
api_router.include_router(category_router, prefix="/category", tags=["Category"])
api_router.include_router(brand_router, prefix="/brand", tags=["Brand"])
api_router.include_router(products_router, prefix="/products", tags=["Products"])
api_router.include_router(cart_router, prefix="/cart", tags=["Cart"])
api_router.include_router(checkout_router, prefix="/checkout", tags=["Checkout"])
api_router.include_router(orders_router, prefix="/orders", tags=["Orders"])
api_router.include_router(rider_router, prefix="/rider", tags=["Rider"])
api_router.include_router(seller_router, prefix="/seller", tags=["Seller"])
api_router.include_router(review_router, prefix="/review", tags=["Review"])
api_router.include_router(notification_router, prefix="/notification", tags=["Notification"])
api_router.include_router(analytics_router, prefix="/analytics", tags=["Analytics"])
api_router.include_router(admin_router, prefix="/admin", tags=["Admin"])
api_router.include_router(ai_router, prefix="/ai", tags=["Ai"])
