import smtplib
import logging
from email.message import EmailMessage
from app.core.config import settings

logger = logging.getLogger(__name__)

def send_reset_password_email(to_email: str, token: str):
    """
    Sends a password reset email securely.
    If SMTP settings are not fully configured in .env, falls back to logging the reset link.
    """
    reset_link = f"{settings.FRONTEND_URL}/reset-password?token={token}"
    
    subject = "Password Reset Request"
    body = f"""Hello,

You have requested to reset your password. 
Please click the link below to set a new password:

{reset_link}

If you did not request this, please ignore this email.
"""

    if not all([settings.SMTP_SERVER, settings.SMTP_PORT, settings.FROM_EMAIL]):
        logger.warning(
            f"\n=== EMAIL NOT SENT (SMTP NOT FULLY CONFIGURED) ===\n"
            f"To: {to_email}\n"
            f"Subject: {subject}\n\n"
            f"{body}\n"
            f"====================================================\n"
            f"Please configure SMTP_SERVER, SMTP_PORT, and FROM_EMAIL in your .env file."
        )
        return

    try:
        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = subject
        msg['From'] = settings.FROM_EMAIL
        msg['To'] = to_email

        with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
            # Most modern SMTP servers support STARTTLS, so try to upgrade
            try:
                server.starttls()
            except Exception:
                pass # If it doesn't support starttls, we just continue (or some servers don't need it)

            if settings.SMTP_USERNAME and settings.SMTP_PASSWORD:
                server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
                
            server.send_message(msg)
            logger.info(f"Password reset email successfully sent to {to_email}")

    except Exception as e:
        logger.error(f"Failed to send password reset email to {to_email}: {e}")
