from datetime import date
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from pet.models import Pet, Image


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ("file",)


class PetSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, required=False, read_only=True)

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
            "owner"
        )

    def validate_images_files(self, files):
        """Базова валідація зображень"""
        if not files:
            return files

        # Перевіряємо що це список
        if not isinstance(files, list):
            raise serializers.ValidationError("Images має бути списком файлів")

        # Перевіряємо що кожен елемент - зображення
        allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif',
                         'image/webp']

        for file in files:
            if not hasattr(file, 'content_type'):
                raise serializers.ValidationError("Невалідний файл")

            if file.content_type not in allowed_types:
                raise serializers.ValidationError(
                    f"Файл {file.name} не є зображенням. "
                    f"Дозволені типи: JPEG, PNG, GIF, WebP"
                )

        return files

    def create(self, validated_data):
        request = self.context.get('request')
        files = request.FILES.getlist('images') if request else []

        # Валідуємо файли
        validated_files = self.validate_images_files(files)

        pet = Pet.objects.create(**validated_data)

        if validated_files:
            images = [Image(pet=pet, file=file) for file in validated_files]
            Image.objects.bulk_create(images)

        return pet



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




class FileSerializer(serializers.Serializer):
    file = serializers.FileField()


class UploadImagesSerializer(serializers.Serializer):
    pet = serializers.IntegerField()
    files = FileSerializer(many=True)


class EmptySerializer(serializers.Serializer):
    pass