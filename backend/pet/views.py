from rest_framework import viewsets

from pet.models import Pet
from pet.serializers import PetSerializer


class PetViewSet(viewsets.ModelViewSet):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
