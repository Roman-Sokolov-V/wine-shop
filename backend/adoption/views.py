from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.viewsets import GenericViewSet, mixins

from adoption.models import Appointment
from adoption.serializers import AppointmentSerializer
from adoption.tasks import send_appointment_task


class AppointmentViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

    def perform_create(self, serializer):
        appointment = serializer.save()
        send_appointment_task.delay_on_commit(
            name=appointment.name,
            email=appointment.email,
            phone=appointment.phone,
            date=appointment.date,
            time=appointment.time,
            add_info=appointment.add_info,
        )

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [AllowAny()]
        else:
            permission_classes = [AllowAny()]
        return permission_classes
