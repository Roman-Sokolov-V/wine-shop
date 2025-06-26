from django.db.models import Max, Min
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, generics, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from pet.filters import PetFilter
from pet.models import Pet
from pet.serializers import (
    PetSerializer,
    UploadImageSerializer,
    EmptySerializer,
    FiltersReportSerializer,
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
        # notify_we_found_pet_for_you(pet=pet, user=user)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

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
        pet = self.get_object()
        user = request.user
        if not user.favorites.filter(pk=pet.pk).exists():
            user.favorites.add(pet)
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        user = request.user
        user.favorites.remove(obj)
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(
    responses=FiltersReportSerializer,
    description="Отримати всі доступні фільтри для тварин",
)
@api_view(["GET"])
@permission_classes([AllowAny])
def filter_report(request):
    """Get filters"""
    breed = Pet.objects.values_list("breed", flat=True).distinct()
    coloration = Pet.objects.values_list("coloration", flat=True).distinct()
    is_sterilized = Pet.objects.values_list("is_sterilized", flat=True).distinct()
    pet_type = Pet.objects.values_list("pet_type", flat=True).distinct()
    sex = ["M", "F", "U"]

    weight_age = Pet.objects.aggregate(
        Max("weight"), Min("weight"), Max("age"), Min("age")
    )
    # pet_type_list = []
    # for type_ in pet_type:
    #     breeds = (
    #         Pet.objects.filter(pet_type=type_)
    #         .values_list("breed", flat=True)
    #         .distinct()
    #     )
    #     pet_type_list.append({type_: {"breed": list(breeds)}})

    data = {
        "breed": list(breed),
        # "pet_type": pet_type_list,
        "pet_type": pet_type,
        "coloration": list(coloration),
        "is_sterilized": list(is_sterilized),
        "sex": list(sex),
        "weight_max": weight_age["weight__max"],
        "weight_min": weight_age["weight__min"],
        "age_max": weight_age["age__max"],
        "age_min": weight_age["age__min"],
    }

    serializer = FiltersReportSerializer(instance=data)
    return Response(serializer.data, status=status.HTTP_200_OK)
