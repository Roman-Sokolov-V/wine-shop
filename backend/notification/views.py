from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAdminUser, AllowAny, SAFE_METHODS
from rest_framework.viewsets import GenericViewSet

from notification.models import Subscription, Mailing
from notification.permissions import IsOwnerOrAdmin
from notification.serializers import SubscriptionSerializer, MailingSerializer


class SubscriptionViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def get_permissions(self):
        if self.action == "destroy":
            return (IsOwnerOrAdmin(),)
        elif self.action == "list":
            return (IsAdminUser(),)
        else:
            return (AllowAny(),)


class MailingViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return (AllowAny(),)
        else:
            return (IsAdminUser(),)
