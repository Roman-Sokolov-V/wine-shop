from rest_framework import viewsets, generics


from pet.models import Pet, Image
from pet.serializers import PetSerializer, UploadImageSerializer


class PetViewSet(viewsets.ModelViewSet):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer


class UploadImageView(generics.ListCreateAPIView):
    queryset = Image.objects.all()
    serializer_class = UploadImageSerializer
