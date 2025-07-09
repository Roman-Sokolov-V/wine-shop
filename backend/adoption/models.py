import datetime

from django.contrib.auth import get_user_model
from django.utils.timezone import now
from django.db import models

from pet.models import Pet

User = get_user_model()


class Appointment(models.Model):
    # name = models.CharField(max_length=100, null=True, blank=True)
    first_name = models.CharField(max_length=255, default="default_name")
    last_name = models.CharField(max_length=255, default="default_name")
    email = models.EmailField()
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="appointments"
    )
    phone = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    add_info = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True, blank=True)

    @staticmethod
    def validate_date_time(
        date: datetime.datetime.date,
        time: datetime.datetime.time,
        error_to_raise,
    ):

        if date < datetime.date.today():
            raise error_to_raise(
                {"date": "Appointment date must be in the future"}
            )

        if date == datetime.date.today() and time <= now().time():
            raise error_to_raise(
                {"time": "Appointment time must be in the future"}
            )

    def clean(self):
        Appointment.validate_date_time(
            self.date,
            self.time,
            ValueError,
        )


STATUS_CHOICES = (
    ("pending", "pending"),
    ("approved", "approved"),
    ("rejected", "rejected"),
)


class AdoptionForm(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="adoption_forms",
    )
    pet = models.ForeignKey(
        Pet,
        on_delete=models.CASCADE,
        related_name="adoption_forms",
    )
    application_date = models.DateField(auto_now_add=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField()
    occupation = models.CharField(max_length=100, blank=True, null=True)
    employer_name = models.CharField(max_length=100, blank=True, null=True)
    employer_phone = models.CharField(max_length=100, blank=True, null=True)
    living_situation = models.TextField(blank=True, null=True)
    household_setting = models.TextField(blank=True, null=True)
    household_members = models.TextField(blank=True, null=True)
    fenced_yard = models.CharField(max_length=255, blank=True, null=True)
    hours_alone = models.IntegerField(blank=True, null=True)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="pending"
    )
