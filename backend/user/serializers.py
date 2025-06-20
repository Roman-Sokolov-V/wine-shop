from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "password",
            "first_name",
            "last_name",
            "is_staff",
            "is_superuser",
            "date_joined",
            "is_active"
        )
        extra_kwargs = {
            "id": {"read_only": True},
            "is_staff": {"read_only": True},
            "is_superuser": {"read_only": True},
            "date_joined": {"read_only": True},
            "is_active": {"read_only": True},
            "password": {"write_only": True, "min_length": 5},
            "email": {"required": True},
        }

    def create(self, validated_data):
        """create User instance"""
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(
        label=_("Email address"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)
    is_superuser = serializers.BooleanField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
