import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import UniqueConstraint

User = get_user_model()


class Mailing(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    run_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title


class Subscription(models.Model):
    mailing = models.ForeignKey(
        Mailing, on_delete=models.CASCADE, related_name="subscriptions"
    )
    email = models.EmailField()
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="subscriptions",
        null=True,
        blank=True,
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["email", "mailing"], name="unique_email_per_mailing"
            ),
            UniqueConstraint(
                fields=["user", "mailing"], name="unique_user_per_mailing"
            ),
        ]
