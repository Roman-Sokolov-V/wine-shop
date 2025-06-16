from rest_framework import viewsets, generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.parsers import MultiPartParser, FormParser

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



class UploadImageView(generics.ListCreateAPIView):
    queryset = Image.objects.all()
    serializer_class = UploadImageSerializer


