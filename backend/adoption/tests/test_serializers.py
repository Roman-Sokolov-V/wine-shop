from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from adoption.serializers import AppointmentSerializer, AdoptionFormSerializer
from datetime import date, time, timedelta
from unittest.mock import patch
from rest_framework.exceptions import ValidationError

from pet.models import Pet

User = get_user_model()


class AppointmentSerializerTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def _make_request(self, user):
        request = self.factory.post("/fake-url/")
        request.user = user
        return request

    @patch("adoption.models.Appointment.validate_date_time")
    def test_validate_date_time_called(self, mock_validate_date_time):
        mock_validate_date_time.side_effect = lambda d, t, e: None

        user = User.objects.create_user(
            email="test@example.com", password="<PASSWORD>"
        )
        data = {
            "date": date.today(),
            "time": time(12, 0),
            "first_name": "Test",
            "last_name": "User",
            "email": "test@example.com",
            "phone": "123456789",
        }
        serializer = AppointmentSerializer(
            data=data, context={"request": self._make_request(user)}
        )
        serializer.is_valid(raise_exception=True)
        mock_validate_date_time.assert_called_once_with(
            data["date"], data["time"], ValidationError
        )

    def test_create_appointment_and_update_user(self):
        user = User.objects.create_user(
            email="test@example.com", password="<PASSWORD>"
        )

        data = {
            "date": date.today() + timedelta(days=1),
            "time": time(10, 30),
            "first_name": "John",
            "last_name": "Doe",
            "phone": "123456789",
            "add_info": "Some info",
        }
        serializer = AppointmentSerializer(
            data=data, context={"request": self._make_request(user)}
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        appointment = serializer.save()

        user.refresh_from_db()
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        self.assertEqual(appointment.email, user.email)
        self.assertEqual(appointment.user, user)

    def test_create_without_first_last_name_sets_from_user(self):
        user = User.objects.create_user(
            email="user2@example.com",
            password="<PASSWORD>",
            first_name="Alice",
            last_name="Smith",
        )
        data = {
            "date": date.today() + timedelta(days=1),
            "time": time(9, 0),
            "phone": "987654321",
            "add_info": "",
        }
        serializer = AppointmentSerializer(
            data=data, context={"request": self._make_request(user)}
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        appointment = serializer.save()
        self.assertEqual(appointment.first_name, user.first_name)
        self.assertEqual(appointment.last_name, user.last_name)
        self.assertEqual(appointment.email, user.email)


class AdoptionFormSerializerTests(TestCase):
    def setUp(self):
        self.pet = Pet.objects.create(name="TestPet", pet_type="Pet")
        self.user = User.objects.create_user(
            email="test@example.com",
            password="STRONG1#password",
        )

    def _make_request(self, user):
        class Request:
            def __init__(self, user):
                self.user = user

        return Request(user)

    def test_create_form_updates_user_if_names_provided(self):
        """User with no names: uses first_name/last_name from form and updates user."""
        self.user.first_name = ""
        self.user.last_name = ""
        self.user.save()

        data = {
            "pet": self.pet.pk,
            "first_name": "John",
            "last_name": "Doe",
            "address": "123 Main St",
            "phone": "1234567890",
        }

        serializer = AdoptionFormSerializer(
            data=data, context={"request": self._make_request(self.user)}
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        form = serializer.save()

        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "John")
        self.assertEqual(self.user.last_name, "Doe")
        self.assertEqual(form.user, self.user)
        self.assertEqual(form.email, self.user.email)

    def test_create_form_uses_user_names_if_present(self):
        """User has names: serializer should ignore provided names and use user’s."""
        self.user.first_name = "Alice"
        self.user.last_name = "Smith"
        self.user.save()

        data = {
            "pet": self.pet.pk,
            "address": "456 Street",
            "phone": "9876543210",
        }

        serializer = AdoptionFormSerializer(
            data=data, context={"request": self._make_request(self.user)}
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        form = serializer.save()

        self.assertEqual(form.first_name, "Alice")
        self.assertEqual(form.last_name, "Smith")

    def test_create_form_fails_without_names(self):
        """No user names, and no names provided → should raise ValidationError."""
        self.user.first_name = ""
        self.user.last_name = ""
        self.user.save()

        data = {
            "pet": self.pet.pk,
            "address": "Unknown",
            "phone": "0000000000",
        }

        serializer = AdoptionFormSerializer(
            data=data, context={"request": self._make_request(self.user)}
        )
        with self.assertRaises(ValidationError) as ctx:
            serializer.is_valid(raise_exception=True)
            serializer.save()

        self.assertIn("first_name", str(ctx.exception))

    def test_create_form_fails_if_anonymous(self):
        """Anonymous user → should raise 403 ValidationError."""

        class AnonymousUser:
            is_authenticated = False

        data = {
            "pet": self.pet.pk,
            "first_name": "Ghost",
            "last_name": "User",
            "address": "Hidden",
            "phone": "1112223333",
        }

        serializer = AdoptionFormSerializer(
            data=data,
            context={"request": self._make_request(AnonymousUser())},
        )
        with self.assertRaises(ValidationError) as ctx:
            serializer.is_valid(raise_exception=True)
            serializer.save()

        self.assertIn("not authorized", str(ctx.exception).lower())
