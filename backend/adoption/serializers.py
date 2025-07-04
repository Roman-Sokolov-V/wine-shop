from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError

from adoption.models import Appointment, AdoptionForm


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
    class Meta:
        model = AdoptionForm
        fields = "__all__"
        extra_kwargs = {
            "application_date": {"read_only": True},
            "user_id": {"read_only": True},
        }

    def get_extra_kwargs(self, *args, **kwargs):
        """
        Returns extra keyword arguments for serializer fields to control their behavior.

        - Makes the 'status' field read-only during creation (when instance is None).
        - For authenticated users, sets 'email' as read-only to prevent client modification.
        - For unauthenticated users, sets 'email' as required to ensure it is provided.

        This approach enforces backend control over sensitive fields while maintaining
        validation requirements based on authentication state.
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
        Automatically assign 'user_id' and 'email' from the authenticated user,
        if available, when creating a new AdoptionForm instance.

        If the user is not authenticated, 'user_id' will remain unset (and can be null).
        This avoids relying on client input for these sensitive fields.
        """
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            validated_data["user_id"] = self.context["request"].user.id
            validated_data["email"] = self.context["request"].user.email
        return super().create(validated_data)

    def validate_pet_id(self, pet_id):
        if not AdoptionForm.objects.filter(id=pet_id).exists():
            raise ValidationError(
                detail=f"Pet with id {pet_id} does not exist.",
                code=status.HTTP_404_NOT_FOUND,
            )


class AdoptionUpdateStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdoptionForm
        fields = ("status",)
