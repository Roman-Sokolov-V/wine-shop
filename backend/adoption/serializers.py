from django.contrib.auth import get_user_model
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError

from adoption.models import Appointment, AdoptionForm
from pet.models import Pet

User = get_user_model()


class AppointmentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Appointment
        fields = "__all__"
        extra_kwargs = {
            "add_info": {"required": False},
            "is_active": {"required": False, "read_only": True},
            "email": {"required": False},
            "first_name": {"required": False},
            "last_name": {"required": False},
            "id": {"read_only": True},
        }

    def validate(self, attrs):
        date = attrs["date"]
        time = attrs["time"]
        Appointment.validate_date_time(
            date,
            time,
            serializers.ValidationError,
        )
        return attrs

    def create(self, validated_data):
        """
        Create a new Appointment instance for an authenticated user.

        - Injects the authenticated user into the `user` field
        of the appointment.
        - Ensures the `email` field is populated from the user's email.
        - Synchronizes `first_name` and `last_name`:
            - If the user already has `first_name` and `last_name`,
            those values are used.
            - Otherwise, values from the request are used to update the user.
            - Raises a ValidationError if either name is missing.
        - Saves the updated user only if any name field was modified.
        - Raises a ValidationError with 403 status code
        if the user is anonymous.

        Args:
            validated_data (dict): The validated data from the serializer.

        Returns:
            Appointment: The newly created Appointment instance.

        Raises:
            ValidationError: If the user is not authenticated, or if
            required fields are missing.
        """
        user = self.context["request"].user
        if user.is_authenticated:
            validated_data["user"] = user
            first_name = validated_data.get("first_name", None)
            last_name = validated_data.get("last_name", None)
            validated_data["email"] = user.email
            user_updated = False
            if user.first_name:
                validated_data["first_name"] = user.first_name
            elif first_name:
                user.first_name = first_name
                user_updated = True
            else:
                raise ValidationError(
                    code=status.HTTP_400_BAD_REQUEST,
                    detail={"first_name": ["This field is required."]},
                )
            if user.last_name:
                validated_data["last_name"] = user.last_name
            elif last_name:
                user.last_name = last_name
                user_updated = True
            else:
                raise ValidationError(
                    code=status.HTTP_400_BAD_REQUEST,
                    detail={"last_name": ["This field is required."]},
                )
            if user_updated:
                user.save()
            return super().create(validated_data)
        raise ValidationError(
            code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to perform this action",
        )


class AdoptionFormSerializer(serializers.ModelSerializer):
    pet = serializers.PrimaryKeyRelatedField(queryset=Pet.objects.all())
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = AdoptionForm
        fields = (
            "id",
            "user",
            "pet",
            "application_date",
            "first_name",
            "last_name",
            "address",
            "phone",
            "email",
            "occupation",
            "employer_name",
            "employer_phone",
            "living_situation",
            "household_setting",
            "household_members",
            "fenced_yard",
            "hours_alone",
            "status",
        )
        extra_kwargs = {
            "application_date": {"read_only": True},
            "user": {"read_only": True},
            "id": {"read_only": True},
            "first_name": {"required": False},
            "last_name": {"required": False},
            "email": {"required": False},
        }

    def get_extra_kwargs(self, *args, **kwargs):
        """
        Returns extra keyword arguments for serializer fields to control
        their behavior.

        - Makes the 'status' field read-only during creation
        (when instance is None).
        - For authenticated users, sets 'email' as read-only to prevent
        client modification.
        - For unauthenticated users, sets 'email' as required to ensure
        it is provided.
        """
        extra_kwargs = super().get_extra_kwargs()
        if self.instance is None:
            extra_kwargs["status"] = {"read_only": True}
        return extra_kwargs

    def create(self, validated_data):
        """
        Create a new AdoptionForm instance for an authenticated user.

        - Assigns the authenticated user to the 'user' field.
        - Populates the 'email' field from the user's email.
        - Synchronizes 'first_name' and 'last_name':
            - If the user already has a name set, that value is used in
            the form.
            - Otherwise, the provided value from the form is used to update
            the user.
            - Raises a ValidationError if either name is missing from both
            the user and the request.
        - Saves the user object only if name data has been updated.
        - Raises a 403 ValidationError if the user is anonymous.

        Args:
            validated_data (dict): The validated data from the serializer.

        Returns:
            AdoptionForm: The newly created AdoptionForm instance.

        Raises:
            ValidationError: If the user is not authenticated or required
            name fields are missing.
        """

        user = self.context["request"].user
        if user.is_authenticated:
            validated_data["user"] = user
            first_name = validated_data.get("first_name", None)
            last_name = validated_data.get("last_name", None)
            validated_data["email"] = user.email
            user_updated = False
            if user.first_name:
                validated_data["first_name"] = user.first_name
            elif first_name:
                user.first_name = first_name
                user_updated = True
            else:
                raise ValidationError(
                    code=status.HTTP_400_BAD_REQUEST,
                    detail={"first_name": ["This field is required."]},
                )
            if user.last_name:
                validated_data["last_name"] = user.last_name
            elif last_name:
                user.last_name = last_name
                user_updated = True
            else:
                raise ValidationError(
                    code=status.HTTP_400_BAD_REQUEST,
                    detail={"last_name": ["This field is required."]},
                )
            if user_updated:
                user.save()
            return super().create(validated_data)
        raise ValidationError(
            code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to perform this action",
        )


class AdoptionUpdateStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdoptionForm
        fields = ("status",)
