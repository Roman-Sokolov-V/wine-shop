from rest_framework.routers import DefaultRouter

from adoption.views import AppointmentViewSet

app_name = "adoption"


router = DefaultRouter()

router.register("appointment", AppointmentViewSet, basename="appointment")

urlpatterns = router.urls
