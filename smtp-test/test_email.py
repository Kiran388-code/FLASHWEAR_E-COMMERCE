import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Read SMTP configuration securely from .env
smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
smtp_port = int(os.getenv("SMTP_PORT", "587"))
sender_email = os.getenv("SMTP_USER", "")
app_password = os.getenv("SMTP_PASSWORD", "")
receiver_email = os.getenv("SMTP_TEST_RECEIVER", sender_email or "your_email@gmail.com")

print("=" * 65)
print("⚡ STANDALONE SMTP CONNECTION & EMAIL DELIVERY TEST")
print("=" * 65)
print(f"SMTP Host:     {smtp_host}:{smtp_port}")
print(f"Sender Email:  {sender_email or '[NOT SET IN .env]'}")
print(f"Receiver Email:{receiver_email}")
print("=" * 65)

if not sender_email or not app_password:
    print("❌ ERROR: SMTP_USER and SMTP_PASSWORD are not set in your .env file.")
    print("Please edit .env and configure your Gmail address and 16-character App Password.")
    print("\nExample .env settings:")
    print("  SMTP_HOST=smtp.gmail.com")
    print("  SMTP_PORT=587")
    print("  SMTP_USER=myproject@gmail.com")
    print("  SMTP_PASSWORD=abcdefghijklmnop")
    print("  SMTP_ENABLED=true")
    exit(1)

message = MIMEText(
    "Hello! This is a test email sent using Python SMTP.\n\n"
    "If you received this message, your Gmail App Password and SMTP connection are configured correctly!",
    "plain"
)

message["Subject"] = "⚡ FLASHWEAR - SMTP Connection Test"
message["From"] = sender_email
message["To"] = receiver_email

try:
    print("1. Connecting to SMTP Server...")
    server = smtplib.SMTP(smtp_host, smtp_port)

    print("2. Starting TLS Encryption...")
    server.starttls()

    print("3. Authenticating with App Password...")
    server.login(sender_email, app_password)

    print("4. Dispatching Email...")
    server.sendmail(sender_email, receiver_email, message.as_string())

    print("5. Closing Connection...")
    server.quit()

    print("\n✅ Email sent successfully! Check the recipient inbox:", receiver_email)

except Exception as e:
    print("\n❌ Email sending failed with error:")
    print(e)
    print("\n💡 Troubleshooting Tips:")
    print("1. Ensure 2-Step Verification is ENABLED on your Google Account.")
    print("2. Ensure you generated a 16-character App Password at https://myaccount.google.com/apppasswords")
    print("3. Do NOT use your normal Gmail password. Use the 16-character App Password.")
