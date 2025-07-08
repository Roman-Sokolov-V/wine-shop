import json
from datetime import datetime, timedelta
from django.utils.timezone import get_current_timezone
from django.utils.timezone import make_aware
from django_celery_beat.models import ClockedSchedule, PeriodicTask
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.viewsets import GenericViewSet, mixins, ModelViewSet

from adoption.models import Appointment, AdoptionForm
from adoption.permissions import IsOwnerOrAdmin
from adoption.serializers import (
    AppointmentSerializer,
    AdoptionFormSerializer,
    AdoptionUpdateStatusSerializer,
)
from adoption.tasks import send_appointment_task, notification_adopt_form


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
            name=appointment.first_name + " " + appointment.last_name,
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
            permission_classes = [IsAuthenticated()]
        else:
            permission_classes = [IsOwnerOrAdmin()]
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


class AdoptionViewSet(ModelViewSet):
    model = AdoptionForm
    queryset = AdoptionForm.objects.all()

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [AllowAny()]
        else:
            permission_classes = [IsOwnerOrAdmin()]
        return permission_classes

    def perform_create(self, serializer):
        form = serializer.save()
        # send emails with form to staff
        notification_adopt_form.delay_on_commit(form.id)

    def get_serializer_class(self):
        if self.action == "partial_update":
            return AdoptionUpdateStatusSerializer
        return AdoptionFormSerializer

    def create(self, request, *args, **kwargs):
        """Create an adoption form"""
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Destroy an adoption form"""
        return super().destroy(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        """List an adoption forms"""
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """Retrieve an adoption form"""
        return super().retrieve(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """Partially update an adoption form"""
        return super().partial_update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """Partially update an adoption form"""
        return super().update(request, *args, **kwargs)
