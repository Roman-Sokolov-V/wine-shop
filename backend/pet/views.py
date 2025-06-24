from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model
from rest_framework import viewsets, generics, permissions, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from notification.notification import notify_we_found_pet_for_you
from pet.filters import PetFilter
from pet.models import Pet, Image
from pet.serializers import (
    PetSerializer,
    UploadImageSerializer,
    EmptySerializer
)


class PetViewSet(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser, FormParser]
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_class = PetFilter

    search_fields = [
        "id",
        "name",
        "pet_type",
        "age",
        "breed",
        "sex",
        "coloration",
        "weight",
        "is_sterilized",
        "owner",
        ]

    def get_queryset(self):
        queryset = Pet.objects.all()
        if self.request.user.is_staff:
            return queryset.select_related("owner")
        return queryset.filter(owner=None)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ["list", "retrieve"]:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    def get_serializer_class(self):
        if self.action == "upload_image":
            return UploadImageSerializer
        return PetSerializer


    def perform_create(self, serializer):
        return serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        pet = self.perform_create(serializer)
        user = get_user_model().objects.first()
        #notify_we_found_pet_for_you(pet=pet, user=user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)

    @action(
        methods=["post"],
        detail=True,
        permission_classes=[permissions.IsAdminUser],
        url_path="upload",
    )
    def upload_image(self, request, pk=None):
        pet = self.get_object()
        data = {
            "file": request.data["file"],
            "pet": pet.pk,
        }
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            image = serializer.save()
            pet.images.add(image)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FavoriteView(generics.GenericAPIView):
    """Add a pet to the authenticated user's favorites."""
    permission_classes = [permissions.IsAuthenticated]
    queryset = Pet.objects.all()
    serializer_class = EmptySerializer

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        user = request.user
        user.favorites.add(obj)
        user.save()
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        user = request.user
        user.favorites.remove(obj)
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
