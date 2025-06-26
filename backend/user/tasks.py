import dramatiq
import logging
from django.contrib.auth import get_user_model

from notification.notification import send_email_restore_password_token
from user.models import TempToken

logger = logging.getLogger(__name__)
User = get_user_model()


@dramatiq.actor
def send_restore_token(token: str, user_email: str):
    try:
        send_email_restore_password_token(token=token, user_email=user_email)
    except Exception as e:
        logger.error(f"Failed to send email to {user_email}: {str(e)}")
        raise
