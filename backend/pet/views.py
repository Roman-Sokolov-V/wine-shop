from django.contrib.auth import get_user_model
from rest_framework import viewsets, generics, permissions, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from notification.notification import notify_we_found_pet_for_you
from pet.filters import PetFilter
from pet.models import Pet, Image
from pet.serializers import PetSerializer, UploadImageSerializer


class PetViewSet(viewsets.ModelViewSet):
    serializer_class = PetSerializer
    parser_classes = [MultiPartParser, FormParser]
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_class = PetFilter
    filterset_fields = [
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

    def perform_create(self, serializer):
        return serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        pet = self.perform_create(serializer)
        print(pet.id)
        user = get_user_model().objects.first()
        notify_we_found_pet_for_you(pet=pet, user=user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)



class UploadImageView(generics.ListCreateAPIView):
    queryset = Image.objects.all()
    serializer_class = UploadImageSerializer
    permission_classes = [permissions.IsAdminUser]


