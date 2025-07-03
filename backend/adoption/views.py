import json
from datetime import datetime, timedelta
from django.utils.timezone import get_current_timezone
from django.utils.timezone import make_aware
from django_celery_beat.models import ClockedSchedule, PeriodicTask
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.viewsets import GenericViewSet, mixins

from adoption.models import Appointment
from adoption.serializers import AppointmentSerializer
from adoption.tasks import send_appointment_task


class AppointmentViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    serializer_class = AppointmentSerializer

    def perform_create(self, serializer):
        appointment = serializer.save()

        # send notifications for staff
        send_appointment_task.delay_on_commit(
            name=appointment.name,
            email=appointment.email,
            phone=appointment.phone,
            date=appointment.date,
            time=appointment.time,
            add_info=appointment.add_info,
        )

        # Create a delayed task to set the appointment status to inactive when it becomes overdue
        clocked_time = datetime.combine(
            appointment.date, appointment.time
        ) + timedelta(hours=2)
        if clocked_time.tzinfo is None:
            clocked_time = make_aware(
                clocked_time, timezone=get_current_timezone()
            )
        clocked, created = ClockedSchedule.objects.get_or_create(
            clocked_time=clocked_time
        )
        PeriodicTask.objects.filter(
            name__startswith=f"set status not active for appointment with id: {appointment.id}"
        ).delete()

        PeriodicTask.objects.create(
            name=f"set status not active for appointment with id: {appointment.id}",
            task="adoption.tasks.set_status_not_active",
            clocked=clocked,
            one_off=True,
            args=json.dumps([appointment.id]),
            enabled=True,
        )

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [AllowAny()]
        else:
            permission_classes = [AllowAny()]
        return permission_classes

    def get_queryset(self):
        if self.action == "active":
            return Appointment.objects.filter(is_active=True)
        else:
            return Appointment.objects.all()

    def create(self, request, *args, **kwargs):
        """Create an appointment"""
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Destroy an appointment"""
        return super().destroy(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        """List an appointment"""
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """Retrieve an appointment"""
        return super().retrieve(request, *args, **kwargs)

    @action(detail=False, methods=["get"])
    def active(self, request, *args, **kwargs):
        """List an active appointment"""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
