from fastapi import APIRouter
from app.api.auth.register import router as register_router
from app.api.auth.login import router as login_router
from app.api.auth.logout import router as logout_router
from app.api.auth.refresh import router as refresh_router
from app.api.auth.forgot_password import router as forgot_password_router
from app.api.auth.reset_password import router as reset_password_router
from app.api.auth.otp import router as otp_router

auth_router = APIRouter()

# Include sub-routes
auth_router.include_router(register_router)
auth_router.include_router(login_router)
auth_router.include_router(logout_router)
auth_router.include_router(refresh_router)
auth_router.include_router(forgot_password_router)
auth_router.include_router(reset_password_router)
auth_router.include_router(otp_router, prefix="/otp")
