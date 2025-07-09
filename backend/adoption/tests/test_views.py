from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.utils.timezone import now, timedelta
from adoption.models import Appointment


User = get_user_model()


def create_user(email, password="testpass", is_staff=False):
    return User.objects.create_user(
        email=email, password=password, is_staff=is_staff
    )


class TestUnauthenticatedAccess(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("adoption:appointment-list")

    def test_create_appointment_denied(self):

        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_appointments_denied(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestAuthenticatedUserAccess(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user("user@example.com")
        self.password = "userpass"
        self.user.set_password(self.password)
        self.user.save()
        self.client.login(email=self.user.email, password=self.password)

        self.appointment = Appointment.objects.create(
            user=self.user,
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            phone="+380123456789",
            date=now().date(),
            time=(now() + timedelta(hours=1)).time(),
            add_info="Info",
            is_active=True,
        )

    def test_create_appointment_success(self):
        self.client.force_authenticate(self.user)
        url = reverse("adoption:appointment-list")
        response = self.client.post(
            url,
            {
                "first_name": "Alice",
                "last_name": "Smith",
                "email": "alice@example.com",
                "phone": "+380987654321",
                "date": now().date(),
                "time": (now() + timedelta(hours=2)).time(),
                "add_info": "Info",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Appointment.objects.count(), 2)

    def test_list_own_appointments_only(self):
        self.client.force_authenticate(self.user)
        url = reverse("adoption:appointment-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["first_name"], "John")

    def test_delete_own_appointment(self):
        self.client.force_authenticate(self.user)
        url = reverse(
            "adoption:appointment-detail", args=[self.appointment.pk]
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_cannot_retrieve_others_appointment(self):
        # створюємо апоінтмент іншого користувача
        other_user = create_user("other@example.com")
        other_appointment = Appointment.objects.create(
            user=other_user,
            first_name="Jane",
            last_name="Roe",
            email="jane@example.com",
            phone="+380999999999",
            date=now().date(),
            time=(now() + timedelta(hours=3)).time(),
            add_info="Other user info",
            is_active=True,
        )

        self.client.force_authenticate(self.user)
        url = reverse(
            "adoption:appointment-detail", args=[other_appointment.pk]
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_cannot_delete_others_appointment(self):
        other_user = create_user("other@example.com")
        other_appointment = Appointment.objects.create(
            user=other_user,
            first_name="Jane",
            last_name="Roe",
            email="jane@example.com",
            phone="+380999999999",
            date=now().date(),
            time=(now() + timedelta(hours=3)).time(),
            add_info="Other user info",
            is_active=True,
        )

        self.client.force_authenticate(self.user)
        url = reverse(
            "adoption:appointment-detail", args=[other_appointment.pk]
        )
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(
            Appointment.objects.filter(id=other_appointment.pk).exists()
        )


class TestAdminAccess(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = create_user("admin@example.com", is_staff=True)
        self.password = "adminpass"
        self.admin.set_password(self.password)
        self.admin.save()
        self.client.force_authenticate(self.admin)

        self.user = create_user("user2@example.com")
        self.appointment = Appointment.objects.create(
            user=self.user,
            first_name="Emma",
            last_name="Brown",
            email="emma@example.com",
            phone="+380123456789",
            date=now().date(),
            time=(now() + timedelta(hours=1)).time(),
            add_info="Test info",
            is_active=True,
        )

    def test_admin_can_list_all_appointments(self):
        url = reverse("adoption:appointment-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["first_name"], "Emma")

    def test_admin_can_access_active_action(self):
        url = reverse("adoption:appointment-active")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.appointment.id, [a["id"] for a in response.data])

    def test_admin_can_delete_any_appointment(self):
        url = reverse(
            "adoption:appointment-detail", args=[self.appointment.pk]
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
