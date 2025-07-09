import json
from datetime import datetime, timedelta
from django.utils.timezone import get_current_timezone
from django.utils.timezone import make_aware
from django_celery_beat.models import ClockedSchedule, PeriodicTask
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiResponse,
)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet, mixins, ModelViewSet

from adoption.models import Appointment, AdoptionForm
from adoption.permissions import IsOwnerOrAdmin
from adoption.serializers import (
    AppointmentSerializer,
    AdoptionFormSerializer,
    AdoptionUpdateStatusSerializer,
)
from adoption.tasks import send_appointment_task, notification_adopt_form


@extend_schema_view(
    list=extend_schema(
        summary="List appointments",
        description="Authenticated users see only their own appointments. Staff users see all.",
        responses={200: AppointmentSerializer(many=True)},
    ),
    retrieve=extend_schema(
        summary="Retrieve an appointment",
        description="Retrieve a single appointment by ID. Only owner or staff can access.",
        responses={200: AppointmentSerializer},
    ),
    create=extend_schema(
        summary="Create an appointment",
        description=(
            "Create a new appointment. Authenticated users only.\n\n"
            "If the user's information (email, name, phone) already exists in the related User instance, "
            "it will automatically be copied into the appointment instance, regardless of the input.\n\n"
            "If this information is not present in the User instance, it must be provided when creating the appointment. "
            "In that case, the data will also be saved to the associated User instance.\n\n"
            "Upon successful creation:\n"
            "- A notification is sent to staff asynchronously.\n"
            "- A scheduled background task is created to automatically deactivate the appointment 2 hours after its scheduled time."
        ),
        responses={201: AppointmentSerializer},
    ),
    destroy=extend_schema(
        summary="Delete an appointment",
        description="Delete an appointment. Only owner or staff can delete.",
        responses={204: OpenApiResponse(description="Deleted successfully")},
    ),
    update=extend_schema(
        summary="Update an appointment",
        description="Fully update a appointment. Only owner or staff.",
        responses={200: AdoptionFormSerializer},
    ),
    partial_update=extend_schema(
        summary="Partially update an appointment",
        description="Used to update status or other fields partially.Only owner or staff.",
        responses={200: AdoptionUpdateStatusSerializer},
    ),
)
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
        """
        Save the appointment instance and perform additional logic:

        1. **Send staff notification** — after saving, an asynchronous task is triggered to notify staff
           via email with the submitted appointment details.

        2. **Schedule a status update** — a delayed periodic task is registered to automatically mark
           the appointment as inactive exactly 2 hours after the scheduled appointment time.

           - If a task with the same name already exists for this appointment, it is removed.
           - The task is one-off and uses a `ClockedSchedule` to execute precisely at the target time.
        """
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
            if not self.request.user.is_staff:
                return Appointment.objects.filter(
                    is_active=True, user=self.request.user
                )
            return Appointment.objects.filter(is_active=True)
        if self.action == "list" and not self.request.user.is_staff:
            return Appointment.objects.filter(user=self.request.user)
        else:
            return Appointment.objects.all()

    @extend_schema(
        summary="List active appointments",
        description=(
            "Custom action. Authenticated users only.\n"
            "- Regular users see only their own active appointments.\n"
            "- Staff users see all active appointments."
        ),
        responses={200: AppointmentSerializer(many=True)},
    )
    @action(detail=False, methods=["get"])
    def active(self, request, *args, **kwargs):
        """List an active appointment"""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema_view(
    list=extend_schema(
        summary="List adoption forms",
        description="Regular users see only their own forms. Staff can see all.",
        responses={200: AdoptionFormSerializer(many=True)},
    ),
    retrieve=extend_schema(
        summary="Retrieve an adoption form",
        description="Retrieve a form by ID. Only owner or staff can access.",
        responses={200: AdoptionFormSerializer},
    ),
    create=extend_schema(
        summary="Create an adoption form",
        description=(
            "Submit a new adoption form. Authenticated users only.\n\n"
            "If the user's information (email, name, phone) already exists in the associated User instance, "
            "it will automatically be copied into the form, regardless of the provided input.\n\n"
            "If this information is missing in the User instance, it must be explicitly provided in the request. "
            "The submitted values will then also be saved to the User instance.\n\n"
            "Upon successful creation:\n"
            "- An asynchronous task is triggered to send a notification email to staff containing the form details."
        ),
        responses={201: AdoptionFormSerializer},
    ),
    destroy=extend_schema(
        summary="Delete an adoption form",
        description="Delete a form. Only owner or staff.",
        responses={204: OpenApiResponse(description="Deleted successfully")},
    ),
    update=extend_schema(
        summary="Update an adoption form",
        description="Fully update a form. Only owner or staff.",
        responses={200: AdoptionFormSerializer},
    ),
    partial_update=extend_schema(
        summary="Partially update an adoption form",
        description="Used to update status or other fields partially.",
        responses={200: AdoptionUpdateStatusSerializer},
    ),
)
class AdoptionViewSet(ModelViewSet):
    model = AdoptionForm
    queryset = AdoptionForm.objects.all()

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [IsAuthenticated()]
        else:
            permission_classes = [IsOwnerOrAdmin()]
        return permission_classes

    def get_queryset(self):
        queryset = self.queryset
        if not self.request.user.is_staff and self.action == "list":
            queryset = queryset.filter(user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        form = serializer.save()
        # send emails with form to staff
        notification_adopt_form.delay_on_commit(form.id)

    def get_serializer_class(self):
        if self.action == "partial_update":
            return AdoptionUpdateStatusSerializer
        return AdoptionFormSerializer
