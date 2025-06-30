from rest_framework import viewsets, mixins, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, AllowAny, SAFE_METHODS
from rest_framework.response import Response
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


@api_view(["post"])
@permission_classes([AllowAny])
def unsubscribe(request):
    token = request.data.get("token")
    if not token:
        return Response(
            {"error": "Token is required"}, status=status.HTTP_400_BAD_REQUEST
        )

    subscription = Subscription.objects.filter(token=token).first()
    if subscription is None:
        return Response(
            {"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST
        )

    subscription.delete()
    return Response(
        {"message": "You have been unsubscribed successfully."},
        status=status.HTTP_200_OK,
    )
