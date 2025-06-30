from django.urls import path
from rest_framework.routers import DefaultRouter
from notification.views import SubscriptionViewSet, MailingViewSet, unsubscribe

app_name = "subscription"


router = DefaultRouter()

router.register("subscriptions", SubscriptionViewSet, basename="subscription")
router.register("mailings", MailingViewSet, basename="mailing")

urlpatterns = [
    path("unsubscribe/", unsubscribe, name="unsubscribe"),
]

urlpatterns += router.urls
