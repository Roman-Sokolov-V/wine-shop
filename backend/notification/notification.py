from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from pet.models import Pet

from django.conf import settings

User = get_user_model()
restore_form_url = settings.FRONT_HOST + settings.RESTORE_FORM_URL


def notify_we_found_pet_for_you(pet: Pet, user: User):

    text_content = render_to_string(
        "emails/found_pet_that_you_looking_for.txt",
        context={"pet": pet, "site_url": "https://example.com"},  # Вказати сайт фронта
    )

    html_content = render_to_string(
        "emails/found_pet_that_you_looking_for.html",
        context={"pet": pet, "site_url": "https://example.com"},  # Вказати сайт фронта
    )

    msg = EmailMultiAlternatives(
        "We have found a pet for you!",
        text_content,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        headers={"List-Unsubscribe": "<mailto:unsub@example.com>"},
    )

    msg.attach_alternative(html_content, "text/html")
    msg.send()


def send_email_restore_password_token(token: str, user_email: str):

    text_content = render_to_string(
        "emails/restore_password.txt",
        context={"token": token, "site_url": restore_form_url},
    )

    html_content = render_to_string(
        "emails/restore_password.html",
        context={"token": token, "site_url": restore_form_url},
    )

    msg = EmailMultiAlternatives(
        "Password Restore",
        text_content,
        settings.DEFAULT_FROM_EMAIL,
        [user_email],
        headers={"List-Unsubscribe": "<mailto:unsub@example.com>"},
    )

    msg.attach_alternative(html_content, "text/html")
    msg.send()


def send_mailing(
    user_email: str, topic: str, content: str, token: str, unscribe_url: str
):

    text_content = render_to_string(
        "emails/mailing_template.txt",
        context={"content": content, "token": token, "unsubscribe_url": unscribe_url},
    )

    html_content = render_to_string(
        "emails/mailing_template.html",
        context={"content": content, "token": token, "unsubscribe_url": unscribe_url},
    )

    msg = EmailMultiAlternatives(
        topic,
        text_content,
        settings.DEFAULT_FROM_EMAIL,
        [user_email],
        headers={"List-Unsubscribe": "<mailto:unsub@example.com>"},
    )

    msg.attach_alternative(html_content, "text/html")
    msg.send()
