from django.urls import path
from rest_framework.routers import DefaultRouter

from adoption.views import AppointmentViewSet

app_name = "adoption"


router = DefaultRouter()

router.register("appointment", AppointmentViewSet, basename="apointment")

urlpatterns = router.urls
