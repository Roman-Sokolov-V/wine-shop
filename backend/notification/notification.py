from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from pet.models import Pet

User = get_user_model()


def notify_we_found_pet_for_you(pet: Pet, user: User):

    text_content = render_to_string(
        "emails/found_pet_that_you_looking_for.txt",
        context={"pet": pet, "site_url": "https://example.com"}, # Вказати сайт фронта
    )

    html_content = render_to_string(
        "emails/found_pet_that_you_looking_for.html",
        context={"pet": pet, "site_url": "https://example.com"},  # Вказати сайт фронта
    )

    msg = EmailMultiAlternatives(
        "We have found a pet for you!",
        text_content,
        "from@example.com",
        [user.email],
        headers={"List-Unsubscribe": "<mailto:unsub@example.com>"},
    )

    msg.attach_alternative(html_content, "text/html")
    msg.send()

def main():
    pet = Pet.objects.first()
    user = User.objects.first()
    notify_we_found_pet_for_you(pet, user)

if __name__ == "__main__":
    main()