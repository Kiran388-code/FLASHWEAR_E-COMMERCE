import secrets
import uuid
import time
from typing import Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.email_verifier import validate_email_address
from app.core.smtp import send_email_async, build_otp_html_email, build_registration_link_html_email
from app.schemas.user import UserCreate
from app.services.user import user_service
from app.repositories.user import user_repository

class OTPService:
    """Service layer for generating and verifying random OTP codes and registration verification links."""
    
    def __init__(self):
        # Memory store: { email: { "otp": "123456", "token": "ver_...", "verified": bool, "expires_at": float } }
        self._otp_store: Dict[str, Dict[str, Any]] = {}
        # Pending registrations store: { email: { "user_in": UserCreate, "token": "ver_reg_...", "expires_at": float } }
        self._pending_registrations: Dict[str, Dict[str, Any]] = {}

    async def send_registration_verification_email(self, db: AsyncSession, user_in: UserCreate) -> Dict[str, Any]:
        """Dispatches an SMTP email containing a unique verification link to confirm user email before registration."""
        email_clean = user_in.email.strip().lower()

        # 1. Check if email already registered in DB
        existing = await user_repository.get_by_email(db, email_clean)
        if existing:
            return {"success": False, "error": "An account with this Email Address is already registered. Please sign in instead."}

        # 2. Email domain validation
        is_real, reason = validate_email_address(email_clean)
        if not is_real:
            return {"success": False, "error": reason}

        # 3. Generate unique verification token
        token = f"ver_reg_{uuid.uuid4().hex}"
        verification_link = f"http://localhost:8000/api/auth/otp/verify-link?token={token}&email={email_clean}"
        expires_at = time.time() + 1800  # Valid for 30 mins

        self._pending_registrations[email_clean] = {
            "user_in": user_in,
            "token": token,
            "verification_link": verification_link,
            "expires_at": expires_at
        }

        # 4. Dispatch Email via SMTP
        html_body = build_registration_link_html_email(
            user_name=user_in.full_name or email_clean.split('@')[0],
            verification_link=verification_link,
            recipient_email=email_clean
        )
        text_body = f"Hello {user_in.full_name},\nPlease click the link below to verify your email and complete registration on FLASHWEAR:\n{verification_link}"

        await send_email_async(
            to_email=email_clean,
            subject="⚡ Verify your email to complete FLASHWEAR registration",
            html_content=html_body,
            text_content=text_body
        )

        return {
            "success": True,
            "email": email_clean,
            "message": f"A verification email has been sent to '{email_clean}'. Please check your inbox and click the verification link to complete registration!"
        }

    async def verify_registration_link(self, db: AsyncSession, token: str, email: str) -> Dict[str, Any]:
        """Verifies email link clicked from user inbox and registers account in Supabase PostgreSQL."""
        email_clean = email.strip().lower()
        pending = self._pending_registrations.get(email_clean)

        if not pending:
            # Check if user was already created
            already_user = await user_repository.get_by_email(db, email_clean)
            if already_user:
                return {"success": True, "message": "Email is already verified! Your account is active. You can now log in."}
            return {"success": False, "error": "No pending registration found for this email address. Please register again."}

        if time.time() > pending["expires_at"]:
            return {"success": False, "error": "Verification link has expired. Please register again to receive a fresh link."}

        if pending["token"] != token.strip():
            return {"success": False, "error": "Invalid or mismatched verification token."}

        user_in: UserCreate = pending["user_in"]

        # Register user in Database
        try:
            created_user = await user_service.register(db, user_in)
            self._pending_registrations.pop(email_clean, None)
            return {
                "success": True,
                "user_id": created_user.id,
                "email": created_user.email,
                "message": f"🎉 Email Verified Successfully! Account for '{created_user.email}' has been created and activated in database. You can now log in!"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def generate_verification_session(self, email: str) -> Dict[str, Any]:
        """Validates real email, generates a random 6-digit OTP and unique token link, and dispatches via SMTP."""
        email_clean = email.strip().lower()
        
        is_real, reason = validate_email_address(email_clean)
        if not is_real:
            return {"success": False, "error": reason}
            
        random_otp = f"{secrets.randbelow(900000) + 100000}"
        token = f"ver_{uuid.uuid4().hex[:16]}"
        expires_at = time.time() + 900
        verification_link = f"http://localhost:8000/api/auth/otp/verify-link?token={token}&email={email_clean}"
        
        session_data = {
            "email": email_clean,
            "otp": random_otp,
            "token": token,
            "verified": False,
            "expires_at": expires_at,
            "verification_link": verification_link
        }
        
        self._otp_store[email_clean] = session_data
        
        html_body = build_otp_html_email(random_otp, verification_link, email_clean)
        text_body = f"Your FLASHWEAR verification code is: {random_otp}\nVerification Link: {verification_link}"
        
        await send_email_async(
            to_email=email_clean,
            subject=f"⚡ {random_otp} is your FLASHWEAR Verification Code",
            html_content=html_body,
            text_content=text_body
        )
        
        return {
            "success": True,
            "email": email_clean,
            "otp": random_otp,
            "token": token,
            "verification_link": verification_link,
            "message": f"Verification email dispatched to {email_clean} with 6-digit OTP."
        }

    def verify_otp_code(self, email: str, code: str) -> Dict[str, Any]:
        """Verifies input 6-digit OTP code."""
        email_clean = email.strip().lower()
        session = self._otp_store.get(email_clean)
        
        if not session:
            return {"success": False, "error": "No verification request found for this email. Please request a new OTP."}
            
        if time.time() > session["expires_at"]:
            return {"success": False, "error": "OTP has expired. Please click resend to get a fresh code."}
            
        if session["otp"] != code.strip():
            return {"success": False, "error": "Incorrect 6-digit OTP code. Please check and try again."}
            
        session["verified"] = True
        return {"success": True, "message": "Email address verified successfully!"}

    def verify_token_link(self, token: str, email: str) -> Dict[str, Any]:
        """Verifies link token parameter."""
        email_clean = email.strip().lower()
        session = self._otp_store.get(email_clean)
        
        if not session:
            return {"success": True, "message": "Verification link accepted! Email verified."}
            
        if session.get("token") == token.strip():
            session["verified"] = True
            return {"success": True, "message": "Email address verified via link!"}
            
        return {"success": False, "error": "Invalid verification token."}

    def is_email_verified(self, email: str) -> bool:
        """Checks whether email has completed verification."""
        email_clean = email.strip().lower()
        session = self._otp_store.get(email_clean)
        return bool(session and session.get("verified"))

otp_service = OTPService()
