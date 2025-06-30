from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from user.tasks import create_subscriptions

User = get_user_model()


@receiver(post_save, sender=User)
def trigger_create_subscriptions(sender, instance, created, **kwargs):
    if created:
        create_subscriptions(instance.email, instance.id)  # celery task
