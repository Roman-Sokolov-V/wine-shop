from rest_framework.routers import DefaultRouter

from adoption.views import AppointmentViewSet, AdoptionViewSet

app_name = "adoption"


router = DefaultRouter()

router.register("adoption_form", AdoptionViewSet, basename="adoption_form")
router.register("appointment", AppointmentViewSet, basename="appointment")


urlpatterns = router.urls
