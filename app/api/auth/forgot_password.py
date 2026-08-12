import uuid
from fastapi import APIRouter
from pydantic import BaseModel, EmailStr
from app.core.smtp import send_email_async, build_password_reset_html_email

router = APIRouter()

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

@router.post("/forgot-password")
async def forgot_password(req: ForgotPasswordRequest) -> dict:
    """Request password reset link/email."""
    token = uuid.uuid4().hex
    reset_link = f"http://localhost:8000/?reset_token={token}&email={req.email}"
    
    html_content = build_password_reset_html_email(reset_link, req.email)
    text_content = f"Password reset link for {req.email}: {reset_link}"
    
    await send_email_async(
        to_email=req.email,
        subject="🔒 FLASHWEAR Password Reset Request",
        html_content=html_content,
        text_content=text_content
    )
    
    return {"message": f"If an account exists for {req.email}, a reset email has been dispatched."}
