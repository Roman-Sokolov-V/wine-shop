from django.urls import path
from rest_framework.routers import DefaultRouter
from notification.views import (
    SubscriptionViewSet,
    MailingViewSet,
    UnsubscribeView,
)

app_name = "subscription"


router = DefaultRouter()

router.register("subscriptions", SubscriptionViewSet, basename="subscription")
router.register("mailings", MailingViewSet, basename="mailing")

urlpatterns = [
    path("unsubscribe/", UnsubscribeView.as_view(), name="unsubscribe"),
]

urlpatterns += router.urls
