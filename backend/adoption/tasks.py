from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.forms import model_to_dict
from django.template.loader import render_to_string

from django.conf import settings

from adoption.models import Appointment, AdoptionForm

User = get_user_model()


@shared_task
def send_appointment_task(
    name: str, email: str, phone: str, date: str, time: str, add_info: str
):
    staffs_emails = User.objects.filter(is_staff=True).values_list(
        "email", flat=True
    )
    for staff_email in staffs_emails:
        text_content = render_to_string(
            "emails/appointment.txt",
            context={
                "name": name,
                "email": email,
                "phone": phone,
                "date": date,
                "time": time,
                "add_info": add_info,
            },
        )

        html_content = render_to_string(
            "emails/appointment.html",
            context={
                "name": name,
                "email": email,
                "phone": phone,
                "date": date,
                "time": time,
                "add_info": add_info,
            },
        )

        msg = EmailMultiAlternatives(
            "new appointment",
            text_content,
            settings.DEFAULT_FROM_EMAIL,
            [staff_email],
            headers={"List-Unsubscribe": "<mailto:unsub@example.com>"},
        )

        msg.attach_alternative(html_content, "text/html")
        msg.send()


@shared_task
def set_status_not_active(
    appointment_id: int,
):
    appointment = Appointment.objects.filter(id=appointment_id).first()
    if appointment:
        appointment.is_active = False
        appointment.save()


@shared_task
def notification_adopt_form(adopt_form_id: int):
    staffs_emails = User.objects.filter(is_staff=True).values_list(
        "email", flat=True
    )
    adopt_form = AdoptionForm.objects.get(id=adopt_form_id)
    context = {"form": model_to_dict(adopt_form)}
    for staff_email in staffs_emails:
        text_content = render_to_string(
            "emails/notification_adopt_form.txt",
            context=context,
        )

        html_content = render_to_string(
            "emails/notification_adopt_form.html",
            context=context,
        )

        msg = EmailMultiAlternatives(
            "new appointment",
            text_content,
            settings.DEFAULT_FROM_EMAIL,
            [staff_email],
            headers={"List-Unsubscribe": "<mailto:unsub@example.com>"},
        )

        msg.attach_alternative(html_content, "text/html")
        msg.send()
