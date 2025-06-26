from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from datetime import timedelta, datetime
from django.utils import timezone

from pet.models import Pet
from user.models import TempToken

User = get_user_model()


class UnauthenticatedUserTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.password = "<PASSWORD>"
        self.db_user = User.objects.create_user(
            email="test@test.com", password=self.password
        )
        self.temp_token = TempToken.objects.create(user=self.db_user)

    def test_users_list(self):
        response = self.client.get(reverse("user:users-list"))
        self.assertEqual(
            status.HTTP_401_UNAUTHORIZED, response.status_code
        ), "Endpoint for staff only"

    def test_get_user(self):
        response = self.client.get(reverse("user:user-detail", kwargs={"pk": 1}))
        self.assertEqual(
            status.HTTP_401_UNAUTHORIZED, response.status_code
        ), "Endpoint for staff only"

    def test_patch_user(self):
        response = self.client.patch(
            reverse("user:user-detail", kwargs={"pk": 1}),
            data={"password": "<newPASSWORD>"},
        )
        self.assertEqual(
            status.HTTP_401_UNAUTHORIZED, response.status_code
        ), "Endpoint for staff only"

    def test_delete_user(self):
        response = self.client.delete(reverse("user:user-detail", kwargs={"pk": 1}))
        self.assertEqual(
            status.HTTP_401_UNAUTHORIZED, response.status_code
        ), "Endpoint for staff only"

    def test_create_user(self):
        response = self.client.post(
            reverse("user:register"),
            data={"email": "new@test.com", "password": "<PASSWORD1d>"},
        )
        self.assertEqual(
            status.HTTP_201_CREATED, response.status_code
        ), "unauthenticated user should be able to create new user"

    def test_login_user_if_registered(self):
        email = self.db_user.email
        password = self.password
        response = self.client.post(
            reverse("user:login"), data={"email": email, "password": password}
        )
        self.assertEqual(
            status.HTTP_200_OK, response.status_code
        ), "unauthenticated user should be able to login if he registered"

    def test_login_user_if_not_registered(self):
        email = "not_exists@email"
        password = self.password
        response = self.client.post(
            reverse("user:login"), data={"email": email, "password": password}
        )
        self.assertEqual(
            status.HTTP_400_BAD_REQUEST, response.status_code
        ), "unauthenticated user can`t login if he not registered"

    def test_login_user_if_invalid_password(self):
        email = self.db_user.email
        password = "invalid_password"
        response = self.client.post(
            reverse("user:login"), data={"email": email, "password": password}
        )

        self.assertEqual(
            status.HTTP_400_BAD_REQUEST, response.status_code
        ), "unauthenticated user can`t login if he not registered"

    def test_logout_user(self):
        response = self.client.post(reverse("user:logout"))
        self.assertEqual(
            status.HTTP_401_UNAUTHORIZED, response.status_code
        ), "unauthenticated user cannot be logged out"

    def test_me(self):
        response = self.client.get(reverse("user:me"))
        (
            self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code),
            "for authenticated user only",
        )

    def test_restore_token(self):
        email = self.db_user.email
        response = self.client.post(
            reverse("user:restore-token"), data={"email": email}
        )
        self.assertEqual(
            status.HTTP_201_CREATED, response.status_code
        ), "unauthenticated user should be able to get restore token if he is registered"

    def test_restore_token_if_email_not_exists(self):
        email = "not_exists@email"
        response = self.client.post(
            reverse("user:restore-token"), data={"email": email}
        )
        self.assertEqual(
            status.HTTP_400_BAD_REQUEST, response.status_code
        ), "unauthenticated user can`t get restore token if invalid email address"

    def test_update_forgotten_password(self):
        email = self.db_user.email
        response = self.client.post(
            reverse("user:restore-token"), data={"email": email}
        )
        self.assertEqual(
            status.HTTP_201_CREATED, response.status_code
        ), "unauthenticated user should be able to get restore token with valid email"

    def test_update_password(self):
        response = self.client.post(
            reverse("user:update-password"),
            data={"token": self.temp_token.key, "password": "<updatedPASSWORD>"},
        )
        self.assertEqual(
            status.HTTP_200_OK, response.status_code
        ), "unauthenticated user should be able to restore password with valid token"

    def test_update_password_if_invalid_token(self):
        invalid_token = "invalid_token"
        response = self.client.post(
            reverse("user:update-password"),
            data={"token": invalid_token, "password": "<updatedPASSWORD>"},
        )
        self.assertEqual(
            status.HTTP_400_BAD_REQUEST, response.status_code
        ), "unauthenticated user can`t restore password with invalid token"

    def test_update_password_if_expired_token(self):
        self.temp_token.created = timezone.now() - timedelta(days=1)
        self.temp_token.save()
        response = self.client.post(
            reverse("user:update-password"),
            data={"token": self.temp_token.key, "password": "<updatedPASSWORD>"},
        )
        self.assertEqual(
            status.HTTP_400_BAD_REQUEST, response.status_code
        ), "unauthenticated user can`t restore password with expired token"


class LoginTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.password = "<PASSWORD>"
        self.data = {
            "email": "test@test.com",
            "password": "<PASSWORD>",
            "first_name": "name",
            "last_name": "last_name",
            "is_staff": True,
            "is_active": True,
            "is_superuser": True,
            "date_joined": str(timezone.now() - timedelta(days=1)),
        }
        self.db_user = User.objects.create_user(**self.data)
        self.token = Token.objects.create(user=self.db_user)
        self.client.force_authenticate(self.db_user, token=self.token.key)
        self.temp_token = TempToken.objects.create(user=self.db_user)
        self.pet = Pet.objects.create(name="Dutch", pet_type="dog")
        self.pet.save()
        self.pet.users_like.add(self.db_user)
        self.pet.save()

    def test_register_user(self):
        data = {
            "email": "test2@test.com",
            "password": "<PASSWORD>",
            "first_name": "name",
            "last_name": "last_name",
            "is_staff": True,
            "is_active": False,
            "is_superuser": True,
            "date_joined": str(timezone.now() - timedelta(days=1)),
        }
        response = self.client.post(reverse("user:register"), data=data)
        self.assertIsNotNone(response.json()["id"])
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(response.json()["email"], data["email"])
        self.assertEqual(response.json()["first_name"], data["first_name"])
        self.assertEqual(response.json()["last_name"], data["last_name"])
        self.assertEqual(
            response.json()["is_staff"], False
        ), "Expected False, if even input True"
        self.assertEqual(
            response.json()["is_active"], True
        ), "Expected True, if even input False"
        self.assertEqual(
            response.json()["is_superuser"], False
        ), "Expected False, if even input True"
        self.assertNotEqual(
            response.json()["date_joined"], data["date_joined"]
        ), "Expected auto_now_add time, not inputted"
        self.assertEqual(response.json()["favorites"], []), "Expected empty list"

    def test_login(self):
        response = self.client.post(
            reverse("user:login"),
            data={"email": self.db_user.email, "password": self.password},
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIsNotNone(response.json()["id"])
        self.assertEqual(response.json()["email"], self.data["email"])
        self.assertEqual(response.json()["first_name"], self.data["first_name"])
        self.assertEqual(response.json()["last_name"], self.data["last_name"])
        self.assertEqual(response.json()["is_staff"], self.data["is_staff"])
        self.assertEqual(response.json()["is_active"], self.data["is_active"])
        self.assertEqual(response.json()["is_superuser"], self.data["is_superuser"])
        date_from_response = datetime.fromisoformat(
            response.json()["date_joined"].replace("Z", "+00:00")
        )
        date_from_data = datetime.fromisoformat(self.data["date_joined"])
        self.assertEqual(date_from_response, date_from_data)
        self.assertIsNone(response.json().get("favorites")), "Expected not exist"

    def test_me(self):
        response = self.client.get(reverse("user:me"))
        self.assertEqual(status.HTTP_200_OK, response.status_code), "200 expected"
        self.assertIsNotNone(response.json()["id"])
        self.assertEqual(response.json()["email"], self.data["email"])
        self.assertEqual(response.json()["first_name"], self.data["first_name"])
        self.assertEqual(response.json()["last_name"], self.data["last_name"])
        self.assertEqual(response.json()["is_staff"], self.data["is_staff"])
        self.assertEqual(response.json()["is_active"], self.data["is_active"])
        self.assertEqual(response.json()["is_superuser"], self.data["is_superuser"])
        date_from_response = datetime.fromisoformat(
            response.json()["date_joined"].replace("Z", "+00:00")
        )
        date_from_data = datetime.fromisoformat(self.data["date_joined"])
        self.assertEqual(date_from_response, date_from_data)
        self.assertEqual(response.json().get("favorites"), [self.pet.id])
