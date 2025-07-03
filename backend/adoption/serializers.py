from rest_framework import serializers
from adoption.models import Appointment


class AppointmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Appointment
        fields = "__all__"
        extra_kwargs = {
            "add_info": {"required": False},
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
