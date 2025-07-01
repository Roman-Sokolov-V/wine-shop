from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers, status

from user.models import TempToken
from django.conf import settings
from user.tasks import create_subscriptions

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    favorites = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    password = serializers.CharField(
        label=_("Password"),
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
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
            "is_active",
            "favorites",
        )
        extra_kwargs = {
            "id": {"read_only": True},
            "is_staff": {"read_only": True},
            "is_superuser": {"read_only": True},
            "date_joined": {"read_only": True},
            "is_active": {"read_only": True},
            "favorites": {"read_only": True},
            "password": {"write_only": True},
            "email": {"required": True},
        }

    def create(self, validated_data):
        """create User instance"""
        return User.objects.create_user(**validated_data)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate_password(self, value):
        validate_password(value)
        return value


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(label=_("Email address"), write_only=True)
    password = serializers.CharField(
        label=_("Password"),
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
    )
    token = serializers.CharField(label=_("Token"), read_only=True)
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)
    is_superuser = serializers.BooleanField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(
                request=self.context.get("request"), email=email, password=password
            )
            if not user:
                msg = _("Unable to log in with provided credentials.")
                raise serializers.ValidationError(msg, code="authorization")
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs


class TempTokenSerializer(serializers.Serializer):
    email = serializers.CharField(
        # label=_("Email address"),
        write_only=True
    )

    def validate(self, attrs):
        email = attrs.get("email")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Not a valid email address.")
        attrs["user"] = user
        return attrs


class UpdatePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        label=_("Password"),
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
        required=True,
        min_length=5,
    )
    token = serializers.CharField(write_only=True, required=True)

    def update(self, instance, validated_data):
        instance.set_password(validated_data["password"])
        instance.save()
        return instance

    def validate(self, attrs):
        token = attrs.get("token")

        try:
            temp_token = TempToken.objects.get(key=token)
        except TempToken.DoesNotExist:
            raise serializers.ValidationError("Token not found in database")

        if timezone.now() > temp_token.created + timedelta(hours=1):
            if settings.DEBUG:
                raise serializers.ValidationError("Restore token has expired")
            else:
                raise serializers.ValidationError(
                    "Token is not valid, or user does not exist"
                )
        attrs["temp_token"] = temp_token
        return attrs
