from rest_framework import serializers

from pet.models import Pet


class PetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = (
            "id",
            "name",
            "type",
            "age",
            "breed",
            "sex",
            "coloration",
            "weight",
            "is_sterilized",
            "description",
            #"owner"
        )
