from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient, force_authenticate
from rest_framework.reverse import reverse
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from datetime import timedelta
from django.utils import timezone

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


class AuthenticatedUserTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.password = "<PASSWORD>"
        self.db_user = User.objects.create_user(
            email="test@test.com", password=self.password
        )
        self.token = Token.objects.create(user=self.db_user)
        self.client.force_authenticate(self.db_user, token=self.token.key)
        self.temp_token = TempToken.objects.create(user=self.db_user)

    def test_users_list(self):
        response = self.client.get(reverse("user:users-list"))
        self.assertEqual(
            status.HTTP_403_FORBIDDEN, response.status_code
        ), "Endpoint for staff only"

    def test_get_user(self):
        response = self.client.get(reverse("user:user-detail", kwargs={"pk": 1}))
        self.assertEqual(
            status.HTTP_403_FORBIDDEN, response.status_code
        ), "Endpoint for staff only"

    def test_patch_user(self):
        response = self.client.patch(
            reverse("user:user-detail", kwargs={"pk": 1}),
            data={"password": "<newPASSWORD>"},
        )
        self.assertEqual(
            status.HTTP_403_FORBIDDEN, response.status_code
        ), "Endpoint for staff only"

    def test_delete_user(self):
        response = self.client.delete(reverse("user:user-detail", kwargs={"pk": 1}))
        self.assertEqual(
            status.HTTP_403_FORBIDDEN, response.status_code
        ), "Endpoint for staff only"

    def test_create_user(self):
        response = self.client.post(
            reverse("user:register"),
            data={"email": "new@test.com", "password": "<PASSWORD1d>"},
        )
        self.assertEqual(
            status.HTTP_201_CREATED, response.status_code
        ), "authenticated user should be able to create new user"

    def test_login_user_if_registered(self):
        email = self.db_user.email
        password = self.password
        response = self.client.post(
            reverse("user:login"), data={"email": email, "password": password}
        )
        self.assertEqual(
            status.HTTP_200_OK, response.status_code
        ), "authenticated user should be able to login if he registered"

    def test_login_user_if_not_registered(self):
        email = "not_exists@email"
        password = self.password
        response = self.client.post(
            reverse("user:login"), data={"email": email, "password": password}
        )
        self.assertEqual(
            status.HTTP_400_BAD_REQUEST, response.status_code
        ), "authenticated user can`t login with invalid email"

    def test_login_user_if_invalid_password(self):
        email = self.db_user.email
        password = "invalid_password"
        response = self.client.post(
            reverse("user:login"), data={"email": email, "password": password}
        )

        self.assertEqual(
            status.HTTP_400_BAD_REQUEST, response.status_code
        ), "authenticated user can`t login with invalid password"

    def test_logout_user(self):

        response = self.client.post(reverse("user:logout"))
        self.assertEqual(
            status.HTTP_200_OK, response.status_code
        ), "authenticated user should be able to logout"
        self.assertEqual("Successfully logged out.", response.json()["detail"])

    def test_logout_user_if_token_missed(self):
        self.token.delete()
        response = self.client.post(reverse("user:logout"))
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual("Token not found for user.", response.json()["detail"])

    def test_me(self):
        response = self.client.get(reverse("user:me"))
        self.assertEqual(status.HTTP_200_OK, response.status_code), "200 expected"

    def test_restore_token(self):
        email = self.db_user.email
        response = self.client.post(
            reverse("user:restore-token"), data={"email": email}
        )
        self.assertEqual(
            status.HTTP_201_CREATED, response.status_code
        ), "authenticated user should be able to get restore token with valid email"

    def test_restore_token_if_email_not_exists(self):
        email = "not_exists@email"
        response = self.client.post(
            reverse("user:restore-token"), data={"email": email}
        )
        self.assertEqual(
            status.HTTP_400_BAD_REQUEST, response.status_code
        ), "authenticated user can`t get restore token if invalid email address"

    def test_update_forgotten_password(self):
        email = self.db_user.email
        response = self.client.post(
            reverse("user:restore-token"), data={"email": email}
        )
        self.assertEqual(
            status.HTTP_201_CREATED, response.status_code
        ), "authenticated user should be able to get restore token with valid email"

    def test_update_password(self):
        response = self.client.post(
            reverse("user:update-password"),
            data={"token": self.temp_token.key, "password": "<updatedPASSWORD>"},
        )
        self.assertEqual(
            status.HTTP_200_OK, response.status_code
        ), "authenticated user should be able to restore password with valid token"

    def test_update_password_if_invalid_token(self):
        invalid_token = "invalid_token"
        response = self.client.post(
            reverse("user:update-password"),
            data={"token": invalid_token, "password": "<updatedPASSWORD>"},
        )
        self.assertEqual(
            status.HTTP_400_BAD_REQUEST, response.status_code
        ), "authenticated user can`t restore password with invalid token"

    def test_update_password_if_expired_token(self):
        self.temp_token.created = timezone.now() - timedelta(days=1)
        self.temp_token.save()
        response = self.client.post(
            reverse("user:update-password"),
            data={"token": self.temp_token.key, "password": "<updatedPASSWORD>"},
        )
        self.assertEqual(
            status.HTTP_400_BAD_REQUEST, response.status_code
        ), "authenticated user can`t restore password with expired token"


class StaffUserTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.password = "<PASSWORD>"
        self.staff_user = User.objects.create_user(
            email="test@test.com", password=self.password
        )
        self.staff_user.is_staff = True
        self.staff_user.save()
        self.regular_user = User.objects.create(
            email="regular@test.com", password="<regularUserPASSWORD>"
        )
        self.token = Token.objects.create(user=self.staff_user)
        self.client.force_authenticate(self.staff_user, token=self.token.key)
        self.temp_token = TempToken.objects.create(user=self.staff_user)

    def test_users_list(self):
        response = self.client.get(reverse("user:users-list"))
        self.assertEqual(
            status.HTTP_200_OK, response.status_code
        ), "Endpoint for staff only"

    def test_get_self_user(self):
        response = self.client.get(
            reverse("user:user-detail", kwargs={"pk": self.staff_user.id}),
        )
        self.assertEqual(
            status.HTTP_200_OK, response.status_code
        ), "Endpoint for staff only"

    def test_get_another_user(self):
        response = self.client.get(
            reverse("user:user-detail", kwargs={"pk": self.regular_user.id}),
        )
        self.assertEqual(
            status.HTTP_200_OK, response.status_code
        ), "Endpoint for staff only"

    def test_patch_user(self):
        response = self.client.patch(
            reverse("user:user-detail", kwargs={"pk": self.regular_user.id}),
            data={"password": "<newPASSWORD>"},
        )
        self.assertEqual(
            status.HTTP_200_OK, response.status_code
        ), "Endpoint for staff only"

    def test_delete_user(self):
        response = self.client.delete(
            reverse("user:user-detail", kwargs={"pk": self.regular_user.id})
        )
        self.assertEqual(
            status.HTTP_204_NO_CONTENT, response.status_code
        ), "Endpoint for staff only"

    def test_create_user(self):
        response = self.client.post(
            reverse("user:register"),
            data={"email": "new@test.com", "password": "<PASSWORD1d>"},
        )
        self.assertEqual(
            status.HTTP_201_CREATED, response.status_code
        ), "staff user should be able to create new user"

    def test_login_user_if_registered(self):
        email = self.staff_user.email
        password = self.password
        response = self.client.post(
            reverse("user:login"), data={"email": email, "password": password}
        )
        self.assertEqual(
            status.HTTP_200_OK, response.status_code
        ), "staff user should be able to login with valid credentials"

    def test_login_user_if_not_registered(self):
        email = "not_exists@email"
        password = self.password
        response = self.client.post(
            reverse("user:login"), data={"email": email, "password": password}
        )
        self.assertEqual(
            status.HTTP_400_BAD_REQUEST, response.status_code
        ), "staff user can`t login with invalid email"

    def test_login_user_if_invalid_password(self):
        email = self.staff_user.email
        password = "invalid_password"
        response = self.client.post(
            reverse("user:login"), data={"email": email, "password": password}
        )

        self.assertEqual(
            status.HTTP_400_BAD_REQUEST, response.status_code
        ), "staff user can`t login with invalid password"

    def test_logout_user(self):

        response = self.client.post(reverse("user:logout"))
        self.assertEqual(
            status.HTTP_200_OK, response.status_code
        ), "staff user should be able to logout"

    def test_me(self):
        response = self.client.get(reverse("user:me"))
        self.assertEqual(status.HTTP_200_OK, response.status_code), "200 expected"

    def test_restore_token(self):
        email = self.staff_user.email
        response = self.client.post(
            reverse("user:restore-token"), data={"email": email}
        )
        self.assertEqual(
            status.HTTP_201_CREATED, response.status_code
        ), "staff user should be able to get restore token with valid email"

    def test_restore_token_if_email_not_exists(self):
        email = "not_exists@email"
        response = self.client.post(
            reverse("user:restore-token"), data={"email": email}
        )
        self.assertEqual(
            status.HTTP_400_BAD_REQUEST, response.status_code
        ), "staff user can`t get restore token if invalid email address"

    def test_update_forgotten_password(self):
        email = self.staff_user.email
        response = self.client.post(
            reverse("user:restore-token"), data={"email": email}
        )
        self.assertEqual(
            status.HTTP_201_CREATED, response.status_code
        ), "staff user should be able to get restore token with valid email"

    def test_update_password(self):
        response = self.client.post(
            reverse("user:update-password"),
            data={"token": self.temp_token.key, "password": "<updatedPASSWORD>"},
        )
        self.assertEqual(
            status.HTTP_200_OK, response.status_code
        ), "staff user should be able to restore password with valid token"

    def test_update_password_if_invalid_token(self):
        invalid_token = "invalid_token"
        response = self.client.post(
            reverse("user:update-password"),
            data={"token": invalid_token, "password": "<updatedPASSWORD>"},
        )
        self.assertEqual(
            status.HTTP_400_BAD_REQUEST, response.status_code
        ), "staff user can`t restore password with invalid token"

    def test_update_password_if_expired_token(self):
        self.temp_token.created = timezone.now() - timedelta(days=1)
        self.temp_token.save()
        response = self.client.post(
            reverse("user:update-password"),
            data={"token": self.temp_token.key, "password": "<updatedPASSWORD>"},
        )
        self.assertEqual(
            status.HTTP_400_BAD_REQUEST, response.status_code
        ), "staff user can`t restore password with expired token"
