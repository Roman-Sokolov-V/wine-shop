from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from backend.user.serializers import UserSerializer, LoginSerializer
from user.permissions import IsOwner

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == "create":
            return [permissions.AllowAny()]
        elif self.action in ["update", "partial_update", "retrieve"]:
            return [permissions.IsAdminUser() | IsOwner()]
        return [permissions.IsAdminUser()]



class LoginView(ObtainAuthToken):
    """
    Login view that return response with TokenAuthentication for
    authentication a user.
    """
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]
