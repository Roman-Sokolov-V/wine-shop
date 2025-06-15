from datetime import date
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from pet.models import Pet, Image


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ("file",)


class PetSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)

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
            "images",
            # "owner"
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


class UploadImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ("pet", "file",)


# class UploadImageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Image
#         fields = ("pet", "file")
#
#     def to_internal_value(self, data):
#         print("RAW DATA:", data)
#         result = super().to_internal_value(data)
#         print("INTERNAL VALUE:", result)
#         return result
#
#     def create(self, validated_data):
#         print("VALIDATED DATA:", validated_data)
#         print("VALIDATED DATA KEYS:", list(validated_data.keys()))
#         print("PET TYPE:", type(validated_data.get('pet')))
#         print("FILE TYPE:", type(validated_data.get('file')))
#
#         try:
#             return Image.objects.create(**validated_data)
#         except Exception as e:
#             print("CREATE ERROR:", str(e))
#             print("ERROR ARGS:", e.args)
#             raise