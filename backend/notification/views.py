from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiResponse,
)
from rest_framework import mixins, status
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from notification.models import Subscription, Mailing
from notification.permissions import IsOwnerOrAdmin
from notification.serializers import (
    SubscriptionSerializer,
    MailingSerializer,
    UnsubscribeSerializer,
)


@extend_schema_view(
    list=extend_schema(
        summary="List all subscriptions",
        description="Admin only. Returns all active subscriptions.",
        responses={200: SubscriptionSerializer(many=True)},
    ),
    create=extend_schema(
        summary="Subscribe",
        description="Open to all users. Creates a new subscription to the "
        "newsletter or notification system.",
        responses={201: SubscriptionSerializer},
    ),
    destroy=extend_schema(
        summary="Unsubscribe",
        description="Authenticated users can delete their own subscriptions. "
        "Admins can delete any.",
        responses={
            204: OpenApiResponse(description="Unsubscribed successfully.")
        },
    ),
)
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


@extend_schema_view(
    list=extend_schema(
        summary="List mailings",
        description="Publicly accessible. Returns a list of active "
        "mailings/newsletters.",
        responses={200: MailingSerializer(many=True)},
    ),
    retrieve=extend_schema(
        summary="Retrieve mailing",
        description="Publicly accessible. Returns a specific "
        "mailing/newsletter by ID.",
        responses={200: MailingSerializer},
    ),
    create=extend_schema(
        summary="Create mailing",
        description="Admin only. Creates a new mailing or newsletter.",
        responses={201: MailingSerializer},
    ),
    destroy=extend_schema(
        summary="Delete mailing",
        description="Admin only. Deletes a mailing by ID.",
        responses={204: OpenApiResponse(description="Deleted successfully.")},
    ),
)
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


@extend_schema(
    summary="Unsubscribe via token",
    description=(
        "Allows users to unsubscribe using a unique token "
        "(e.g., from email link).\n"
        "No authentication is required. If the token is valid, the related "
        "subscription will be deleted."
    ),
    request=UnsubscribeSerializer,
    responses={
        200: OpenApiResponse(description="Unsubscribed successfully."),
        400: OpenApiResponse(description="Invalid or expired token."),
    },
)
class UnsubscribeView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UnsubscribeSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data["token"]

        subscription = Subscription.objects.filter(token=token).first()
        if subscription is None:
            return Response(
                {"error": "Invalid or expired token"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        subscription.delete()
        return Response(
            {"message": "You have been unsubscribed successfully."},
            status=status.HTTP_200_OK,
        )
