import datetime
from django.utils.timezone import now
from django.db import models


class Appointment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    add_info = models.TextField(blank=True, null=True)

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
