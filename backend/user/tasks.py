import dramatiq
import logging

from celery import shared_task
from django.contrib.auth import get_user_model

import user
from notification.models import Mailing, Subscription
from notification.notification import send_email_restore_password_token
from user.models import TempToken

logger = logging.getLogger(__name__)
User = get_user_model()


@shared_task
def send_restore_token(token: str, user_email: str):
    """send email with token for update forgotten password"""
    try:
        send_email_restore_password_token(
            token=token, user_email=user_email
        )  # celery task
    except Exception as e:
        logger.error(f"Failed to send email to {user_email}: {str(e)}")
        raise


@shared_task
def create_subscriptions(email: str, user_id: int) -> None:
    """create subscriptions with all mailing"""
    mailings_ids = Mailing.objects.all().values_list("id", flat=True)
    if mailings_ids:
        Subscription.objects.bulk_create(
            (
                Subscription(
                    email=email, mailing_id=mailing_id, user_id=user_id
                )
                for mailing_id in mailings_ids
            )
        )
