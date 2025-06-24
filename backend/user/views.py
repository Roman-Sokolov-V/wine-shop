from django.contrib.auth import get_user_model

from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, extend_schema_view

from notification.notification import send_email_restore_password_token
from user.models import TempToken
from user.serializers import (
    UserSerializer,
    LoginSerializer,
    TempTokenSerializer,
    UpdatePasswordSerializer,
)
from user.permissions import IsOwner
from user.tasks import send_restore_token

User = get_user_model()


@extend_schema_view(
    list=extend_schema(description="Get the list of all users."),
    retrieve=extend_schema(description="Retrieve a specific user by ID."),
    create=extend_schema(description="Create a new user."),
    update=extend_schema(description="Fully update a user."),
    partial_update=extend_schema(description="Partially update a user."),
    destroy=extend_schema(description="Delete a user."),
)
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == "create":
            return [permissions.AllowAny()]
        elif self.action in ["update", "partial_update", "retrieve"]:
            return [permissions.OR(permissions.IsAdminUser(), IsOwner())]
        return [permissions.IsAdminUser()]


class LoginView(ObtainAuthToken):
    """
    Login view that return response with TokenAuthentication and user data.
    """

    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key,
                "id": user.pk,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "is_staff": user.is_staff,
                "is_superuser": user.is_superuser,
                "is_active": user.is_active,
                "date_joined": user.date_joined,
            }
        )


class LogoutView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        """
        Logout the authenticated user by deleting their token.
        """
        try:
            token = Token.objects.get(user=request.user)
            token.delete()
            return Response(
                {"detail": "Successfully logged out."}, status=status.HTTP_200_OK
            )
        except Token.DoesNotExist:
            return Response(
                {"detail": "Token not found for user."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"detail": f"An error occurred: {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class MeView(generics.GenericAPIView):
    """Show authenticated user data"""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)


@extend_schema(request=TempTokenSerializer, responses={201: None})
class TemporaryTokenView(APIView):
    """
    Endpoint to create a temporary token to update forgotten password
    """

    permission_classes = [permissions.AllowAny]
    serializer_class = TempTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        user = validated_data["user"]
        TempToken.objects.filter(user=user).delete()
        token = TempToken.objects.create(user=user)
        # send_email_restore_password_token(token=token.key, user=user)
        send_restore_token.send(token=token.key, user_email=user.email)
        return Response(status=status.HTTP_201_CREATED)


class UpdatePasswordView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UpdatePasswordSerializer
    """
    Endpoint to update forgotten password
    """

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            temp_token = validated_data["temp_token"]
            user = temp_token.user
            serializer.update(instance=user, validated_data=validated_data)
            temp_token.delete()
            return Response(
                {"detail": "Password has been updated"}, status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
