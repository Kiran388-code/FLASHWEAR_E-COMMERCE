import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.core.config import settings
from app.core.exceptions import CustomAppException, app_exception_handler
from app.core.middleware import RequestLoggingMiddleware
from app.lifespan import lifespan
from app.api import api_router

app = FastAPI(
    title=settings.APP_NAME,
    description="Production-grade API & Quick Commerce Platform for FLASHWEAR.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request execution logging middleware
app.add_middleware(RequestLoggingMiddleware)

# Global custom app exception handler
app.add_exception_handler(CustomAppException, app_exception_handler)

# Include core api routing table
app.include_router(api_router, prefix="/api")

# Mount Static directory
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/", include_in_schema=False)
async def serve_customer_portal():
    return FileResponse(os.path.join(static_dir, "index.html"))

@app.get("/seller", include_in_schema=False)
async def serve_seller_portal():
    seller_file = os.path.join(static_dir, "seller.html")
    if os.path.exists(seller_file):
        return FileResponse(seller_file)
    return {"message": "Seller Partner Portal HTML file not found."}

@app.get("/rider", include_in_schema=False)
async def serve_rider_portal():
    rider_file = os.path.join(static_dir, "rider.html")
    if os.path.exists(rider_file):
        return FileResponse(rider_file)
    return {"message": "Rider Portal HTML file not found."}

@app.get("/admin", include_in_schema=False)
async def serve_admin_portal():
    admin_file = os.path.join(static_dir, "admin.html")
    if os.path.exists(admin_file):
        return FileResponse(admin_file)
    return {"message": "Admin Portal HTML file not found."}

@app.get("/styles.css", include_in_schema=False)
async def serve_styles():
    return FileResponse(os.path.join(static_dir, "styles.css"))

@app.get("/app.js", include_in_schema=False)
async def serve_app_js():
    return FileResponse(os.path.join(static_dir, "app.js"))

@app.get("/api.js", include_in_schema=False)
async def serve_api_js():
    return FileResponse(os.path.join(static_dir, "api.js"))

@app.get("/health", tags=["System health check"])
async def health() -> dict:
    """Returns application health status."""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "environment": settings.ENVIRONMENT
    }
