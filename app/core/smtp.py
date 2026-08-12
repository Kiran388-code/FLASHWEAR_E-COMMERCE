import smtplib
import asyncio
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
from app.core.config import settings

logger = logging.getLogger("flashwear.smtp")

def send_email_sync(
    to_email: str, 
    subject: str, 
    html_content: str, 
    text_content: Optional[str] = None
) -> bool:
    """
    Sends an email using standard smtplib.
    Supports STARTTLS (587) and SSL (465).
    """
    if not settings.SMTP_ENABLED or not settings.SMTP_USER or not settings.SMTP_PASSWORD:
        logger.info(
            f"📧 [SMTP MOCK MODE] Email to '{to_email}' skipped (SMTP credentials not configured).\n"
            f"Subject: {subject}\n"
            f"HTML Length: {len(html_content)} bytes"
        )
        return True

    try:
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = f"{settings.SMTP_FROM_NAME} <{settings.SMTP_FROM_EMAIL}>"
        message["To"] = to_email

        if text_content:
            part1 = MIMEText(text_content, "plain")
            message.attach(part1)

        part2 = MIMEText(html_content, "html")
        message.attach(part2)

        if settings.SMTP_SSL or settings.SMTP_PORT == 465:
            with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.sendmail(settings.SMTP_FROM_EMAIL, to_email, message.as_string())
        else:
            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                if settings.SMTP_TLS:
                    server.starttls()
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.sendmail(settings.SMTP_FROM_EMAIL, to_email, message.as_string())

        logger.info(f"✅ SMTP Email successfully sent to {to_email}")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to send SMTP email to {to_email}: {e}")
        return False

async def send_email_async(
    to_email: str, 
    subject: str, 
    html_content: str, 
    text_content: Optional[str] = None
) -> bool:
    """Asynchronous wrapper for email delivery to prevent blocking the event loop."""
    return await asyncio.to_thread(
        send_email_sync, to_email, subject, html_content, text_content
    )

def build_otp_html_email(otp_code: str, verification_link: str, recipient_email: str) -> str:
    """Returns a styled HTML template for OTP verification."""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; background-color: #0f172a; color: #f8fafc; margin: 0; padding: 20px; }}
        .card {{ max-width: 500px; margin: 0 auto; background: #1e293b; border-radius: 12px; border: 1px solid #334155; padding: 32px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); }}
        .header {{ text-align: center; margin-bottom: 24px; }}
        .brand {{ font-size: 24px; font-weight: 800; color: #6366f1; letter-spacing: 1px; }}
        .otp-box {{ background: #0f172a; border-radius: 8px; padding: 16px; text-align: center; font-size: 32px; font-weight: 900; letter-spacing: 8px; color: #10b981; margin: 20px 0; border: 1px dashed #10b981; }}
        .btn {{ display: block; text-align: center; background: #6366f1; color: #ffffff !important; padding: 14px 24px; border-radius: 8px; text-decoration: none; font-weight: 700; margin-top: 20px; }}
        .footer {{ font-size: 12px; color: #64748b; text-align: center; margin-top: 24px; }}
      </style>
    </head>
    <body>
      <div class="card">
        <div class="header">
          <div class="brand">⚡ FLASHWEAR</div>
          <h2 style="color: #f8fafc; margin-top: 8px;">Verify Your Email Address</h2>
        </div>
        <p>Hello,</p>
        <p>Use the 6-digit verification code below to complete your registration or login for <strong>{recipient_email}</strong>:</p>
        
        <div class="otp-box">{otp_code}</div>
        
        <p style="text-align: center; font-size: 13px; color: #94a3b8;">Or click the instant 1-click verification link below:</p>
        <a href="{verification_link}" class="btn" target="_blank">Verify Email Instantly 🚀</a>
        
        <div class="footer">
          This verification code expires in 15 minutes.<br>
          If you did not request this email, you can safely ignore it.
        </div>
      </div>
    </body>
    </html>
    """

def build_password_reset_html_email(reset_link: str, recipient_email: str) -> str:
    """Returns a styled HTML template for password reset."""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; background-color: #0f172a; color: #f8fafc; margin: 0; padding: 20px; }}
        .card {{ max-width: 500px; margin: 0 auto; background: #1e293b; border-radius: 12px; border: 1px solid #334155; padding: 32px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); }}
        .header {{ text-align: center; margin-bottom: 24px; }}
        .brand {{ font-size: 24px; font-weight: 800; color: #6366f1; letter-spacing: 1px; }}
        .btn {{ display: block; text-align: center; background: #ec4899; color: #ffffff !important; padding: 14px 24px; border-radius: 8px; text-decoration: none; font-weight: 700; margin-top: 20px; }}
        .footer {{ font-size: 12px; color: #64748b; text-align: center; margin-top: 24px; }}
      </style>
    </head>
    <body>
      <div class="card">
        <div class="header">
          <div class="brand">⚡ FLASHWEAR</div>
          <h2 style="color: #f8fafc; margin-top: 8px;">Reset Your Password</h2>
        </div>
        <p>Hello,</p>
        <p>We received a request to reset the password for account <strong>{recipient_email}</strong>.</p>
        
        <a href="{reset_link}" class="btn" target="_blank">Reset Password 🔒</a>
        
        <div class="footer">
          If you did not request a password reset, please ignore this email.<br>
          Your password will remain unchanged.
        </div>
      </div>
    </body>
    </html>
    """

def build_registration_link_html_email(user_name: str, verification_link: str, recipient_email: str) -> str:
    """Returns a styled HTML template for email verification link sent during new user registration."""
    template = """
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <style>
        body { font-family: 'Segoe UI', Arial, sans-serif; background-color: #0f172a; color: #f8fafc; margin: 0; padding: 20px; }
        .card { max-width: 520px; margin: 0 auto; background: #1e293b; border-radius: 16px; border: 1px solid #334155; padding: 36px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
        .header { text-align: center; margin-bottom: 24px; }
        .brand { font-size: 26px; font-weight: 800; color: #6366f1; letter-spacing: 1px; }
        .btn { display: block; text-align: center; background: linear-gradient(135deg, #6366f1, #8b5cf6); color: #ffffff !important; padding: 16px 28px; border-radius: 10px; text-decoration: none; font-weight: 800; font-size: 16px; margin: 24px 0; box-shadow: 0 4px 14px rgba(99,102,241,0.4); }
        .footer { font-size: 12px; color: #64748b; text-align: center; margin-top: 28px; border-top: 1px solid #334155; padding-top: 16px; }
      </style>
    </head>
    <body>
      <div class="card">
        <div class="header">
          <div class="brand">⚡ FLASHWEAR</div>
          <h2 style="color: #f8fafc; margin-top: 10px;">Verify Email & Complete Registration</h2>
        </div>
        <p>Welcome <strong>{{USER_NAME}}</strong>,</p>
        <p>Thank you for creating an account on FLASHWEAR! To confirm your email address (<strong>{{RECIPIENT_EMAIL}}</strong>) and activate your profile in our database, please click the button below:</p>
        
        <a href="{{VERIFICATION_LINK}}" class="btn" target="_blank">Verify My Email & Complete Registration 🚀</a>
        
        <p style="font-size: 13px; color: #94a3b8; word-break: break-all;">If the button doesn't work, copy and paste this link into your browser:<br><a href="{{VERIFICATION_LINK}}" style="color: #818cf8;">{{VERIFICATION_LINK}}</a></p>

        <div class="footer">
          This verification link is valid for 30 minutes.<br>
          If you did not attempt to register on FLASHWEAR, please ignore this email.
        </div>
      </div>
    </body>
    </html>
    """
    return template.replace("{{USER_NAME}}", user_name)\
                   .replace("{{VERIFICATION_LINK}}", verification_link)\
                   .replace("{{RECIPIENT_EMAIL}}", recipient_email)
