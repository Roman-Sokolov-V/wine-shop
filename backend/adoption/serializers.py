from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError

from adoption.models import Appointment, AdoptionForm
from pet.models import Pet


class AppointmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Appointment
        fields = "__all__"
        extra_kwargs = {
            "add_info": {"required": False},
            "is_active": {"required": False, "read_only": True},
            "email": {"required": True},
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
        }

    def get_extra_kwargs(self, *args, **kwargs):
        """
        Returns extra keyword arguments for serializer fields to control their behavior.

        - Makes the 'status' field read-only during creation (when instance is None).
        - For authenticated users, sets 'email' as read-only to prevent client modification.
        - For unauthenticated users, sets 'email' as required to ensure it is provided.
        """
        extra_kwargs = super().get_extra_kwargs()
        if self.instance is None:
            extra_kwargs["status"] = {"read_only": True}

        request = self.context.get("request")
        if request and request.user.is_authenticated:
            extra_kwargs["email"] = {"read_only": True}
        else:
            extra_kwargs["email"] = {"required": True}
        return extra_kwargs

    def create(self, validated_data):
        """
        Automatically assign 'user' and 'email' from the authenticated user,
        if available, when creating a new AdoptionForm instance.

        If the user is not authenticated, 'user' will remain unset (and can be null).
        """
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            validated_data["user"] = request.user
            validated_data["email"] = request.user.email
        return super().create(validated_data)


class AdoptionUpdateStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdoptionForm
        fields = ("status",)
