from celery import shared_task

from notification.models import Subscription
from notification.notification import send_mailing

from django.conf import settings

FULL_UNSUBSCRIBE_URL = settings.FRONT_HOST + settings.UNSUBSCRIBE_URL

@shared_task
def send_mailing_task(mailing_id: int):

    subscriptions = Subscription.objects.filter(mailing_id=mailing_id).select_related(
        "user", "mailing"
    )
    for subscription in subscriptions:
        email = subscription.email or (
            subscription.user.email if subscription.user else None
        )
        if not email:
            continue  # або логувати warning
        send_mailing(
            user_email=email,
            topic=subscription.mailing.title,
            content=subscription.mailing.content,
            token=subscription.token,
            unsubscribe_url=FULL_UNSUBSCRIBE_URL
        )
