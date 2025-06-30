from django.contrib import admin
from .models import Subscription, Mailing

admin.site.register(Mailing)
admin.site.register(Subscription)
