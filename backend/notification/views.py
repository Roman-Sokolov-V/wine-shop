from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAdminUser, AllowAny
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


class MailingViewSet(viewsets.ModelViewSet):
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer
    permission_classes = (IsAdminUser,)
