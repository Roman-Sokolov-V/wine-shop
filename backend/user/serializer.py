from django.contrib.auth import get_user_model

from rest_framework import serializers


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id", "email", "password", "first_name", "last_name", "is_staff"
        )
        extra_kwargs = {
            "id": {"read_only": True},
            "is_staff": {"read_only": True},
            "password": {"write_only": True, "min_length": 5},
            "email": {"required": True},
        }

    def create(self, validated_data):
        """create User instance"""
        return User.objects.create_user(**validated_data)


