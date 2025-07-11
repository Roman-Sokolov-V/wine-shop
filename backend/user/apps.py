from django.apps import AppConfig
from django.db.models.signals import post_save


class UserConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "user"

    def ready(self):
        from . import signals
