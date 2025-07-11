from django.contrib import admin

from adoption.models import Appointment, AdoptionForm

# Register your models here.
admin.site.register(Appointment)

admin.site.register(AdoptionForm)
