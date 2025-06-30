import json

from django.db.models.signals import post_save
from django.dispatch import receiver
from django_celery_beat.models import ClockedSchedule, PeriodicTask
from django.utils.timezone import make_aware
from notification.models import Mailing


@receiver(post_save, sender=Mailing)
def trigger_create_update_mailing(sender, instance, created, **kwargs):
    clocked_time = instance.run_at
    if clocked_time.tzinfo is None:
        from django.utils.timezone import get_current_timezone

        clocked_time = make_aware(clocked_time, timezone=get_current_timezone())

    clocked, created = ClockedSchedule.objects.get_or_create(clocked_time=clocked_time)

    PeriodicTask.objects.filter(
        name__startswith=f"One-off mailing {instance.id}"
    ).delete()

    PeriodicTask.objects.create(
        name=f"One-off mailing {instance.id}, {instance.title}",
        task="notification.tasks.send_mailing_task",
        clocked=clocked,
        one_off=True,
        args=json.dumps([instance.id]),  # передаємо аргументи
        enabled=True,
    )
