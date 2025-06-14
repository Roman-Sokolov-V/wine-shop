from datetime import date
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


from pet.models import Pet


class PetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = (
            "id",
            "name",
            "pet_type",
            "age",
            "breed",
            "sex",
            "coloration",
            "weight",
            "is_sterilized",
            "description",
            #"owner"
        )

    def validate(self, data):
        if self.instance is None:
            name = data.get("name")
            pet_type = data.get("pet_type")
            age = data.get("age")
            breed = data.get("breed")
            sex = data.get("sex")
            coloration = data.get("coloration")
            weight = data.get("weight")
            is_sterilized = data.get("is_sterilized")
            description = data.get("description")
            date_added = date.today()

            if Pet.objects.filter(
                name=name,
                pet_type=pet_type,
                age=age,
                breed=breed,
                sex=sex,
                coloration=coloration,
                weight=weight,
                is_sterilized=is_sterilized,
                description=description,
                date_created=date_added,

            ).exists():
                raise ValidationError(
                    "Pet with the same parameters already added to db today. "
                    "Make sure you not try to add the same pet by mistake. "
                    "If not just change any field"
                )
                return data