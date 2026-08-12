from fastapi import APIRouter, HTTPException, Query, Depends
from pydantic import BaseModel, Field
from app.services.otp_service import otp_service
from app.core.email_verifier import validate_email_address

router = APIRouter()

class SendOTPRequest(BaseModel):
    contact: str = Field(..., description="Email address to send verification to")

class VerifyOTPRequest(BaseModel):
    contact: str
    code: str = Field(..., min_length=4, max_length=8)

@router.post("/send")
async def send_otp(req: SendOTPRequest) -> dict:
    """Validates real vs fake email domain, generates a random 6-digit OTP & verification link."""
    res = await otp_service.generate_verification_session(req.contact)
    if not res["success"]:
        raise HTTPException(status_code=400, detail=res["error"])
    return res

@router.post("/verify")
async def verify_otp(req: VerifyOTPRequest) -> dict:
    """Verifies input 6-digit OTP code."""
    res = otp_service.verify_otp_code(req.contact, req.code)
    if not res["success"]:
        raise HTTPException(status_code=400, detail=res["error"])
    return res

from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_db_session

@router.get("/verify-link", response_class=HTMLResponse)
async def verify_link(
    token: str = Query(...), 
    email: str = Query(...),
    db: AsyncSession = Depends(get_db_session)
):
    """Verifies email verification URL link sent via SMTP, activates account in database, and returns styled HTML page."""
    # Check registration link verification first
    if token.startswith("ver_reg_"):
        res = await otp_service.verify_registration_link(db, token, email)
    else:
        res = otp_service.verify_token_link(token, email)

    if res.get("success"):
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
          <title>FLASHWEAR Email Verified</title>
          <style>
            body {{ font-family: 'Segoe UI', system-ui, sans-serif; background: #0f172a; color: #f8fafc; display: grid; place-items: center; min-height: 100vh; margin: 0; padding: 20px; }}
            .card {{ background: #1e293b; border-radius: 24px; border: 1px solid #334155; padding: 48px; text-align: center; max-width: 500px; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.5); }}
            .icon {{ font-size: 64px; margin-bottom: 16px; }}
            h1 {{ font-size: 26px; font-weight: 800; color: #10b981; margin-bottom: 12px; }}
            p {{ color: #94a3b8; font-size: 15px; line-height: 1.6; margin-bottom: 28px; }}
            .btn {{ display: inline-block; background: linear-gradient(135deg, #6366f1, #8b5cf6); color: white !important; padding: 14px 32px; border-radius: 12px; font-weight: 800; text-decoration: none; font-size: 16px; box-shadow: 0 4px 14px rgba(99,102,241,0.4); }}
          </style>
        </head>
        <body>
          <div class="card">
            <div class="icon">🎉</div>
            <h1>Email Verified Successfully!</h1>
            <p>{res.get("message")}</p>
            <a href="http://localhost:8000" class="btn">Return to FLASHWEAR & Sign In 🛍️</a>
          </div>
        </body>
        </html>
        """
    else:
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
          <title>FLASHWEAR Verification Error</title>
          <style>
            body {{ font-family: 'Segoe UI', system-ui, sans-serif; background: #0f172a; color: #f8fafc; display: grid; place-items: center; min-height: 100vh; margin: 0; padding: 20px; }}
            .card {{ background: #1e293b; border-radius: 24px; border: 1px solid #ef4444; padding: 48px; text-align: center; max-width: 500px; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.5); }}
            .icon {{ font-size: 64px; margin-bottom: 16px; }}
            h1 {{ font-size: 26px; font-weight: 800; color: #ef4444; margin-bottom: 12px; }}
            p {{ color: #94a3b8; font-size: 15px; line-height: 1.6; margin-bottom: 28px; }}
            .btn {{ display: inline-block; background: #334155; color: white !important; padding: 14px 32px; border-radius: 12px; font-weight: 800; text-decoration: none; font-size: 16px; }}
          </style>
        </head>
        <body>
          <div class="card">
            <div class="icon">❌</div>
            <h1>Verification Failed</h1>
            <p>{res.get("error")}</p>
            <a href="http://localhost:8000" class="btn">Return to Home Page</a>
          </div>
        </body>
        </html>
        """

@router.post("/validate-email")
async def validate_email(req: SendOTPRequest) -> dict:
    """Checks whether an email is properly formatted and from a real domain."""
    is_valid, reason = validate_email_address(req.contact)
    if not is_valid:
        raise HTTPException(status_code=400, detail=reason)
    return {"valid": True, "message": reason}
