from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

from pet.models import Pet

User = get_user_model()


small_gif = (
    b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00"
    b"\xff\xff\xff\x21\xf9\x04\x00\x00\x00\x00\x00\x2c\x00\x00\x00\x00"
    b"\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b"
)


class UnauthenticatedUserTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.password = "<PASSWORD>"
        self.db_user = User.objects.create_user(
            email="test@test.com", password=self.password
        )
        self.pet = Pet.objects.create(name="test", pet_type="cat")

    def test_pets_list(self):
        response = self.client.get(reverse("pet:pets-list"))
        self.assertEqual(status.HTTP_200_OK, response.status_code), "for all users"

    def test_get_pet(self):
        response = self.client.get(
            reverse("pet:pet-detail", kwargs={"pk": self.pet.pk})
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code), "for all users"

    def test_create_pet(self):
        response = self.client.post(
            reverse("pet:pets-list"), data={"name": "Tom", "pet_type": "cat"}
        )
        self.assertEqual(
            status.HTTP_401_UNAUTHORIZED, response.status_code
        ), "for staff only"

    def test_patch_pet(self):
        response = self.client.patch(
            reverse("pet:pet-detail", kwargs={"pk": self.pet.pk}),
            data={"nae": "newName"},
        )
        self.assertEqual(
            status.HTTP_401_UNAUTHORIZED, response.status_code
        ), "Endpoint for staff only"

    def test_delete_user(self):
        response = self.client.delete(
            reverse("pet:pet-detail", kwargs={"pk": self.pet.pk})
        )
        self.assertEqual(
            status.HTTP_401_UNAUTHORIZED, response.status_code
        ), "Endpoint for staff only"

    def test_upload_image(self):
        url = reverse("pet:pet-upload-image", kwargs={"pk": self.pet.pk})
        response = self.client.post(url)
        self.assertEqual(
            status.HTTP_401_UNAUTHORIZED, response.status_code
        ), "Endpoint for staff only"

    def test_add_to_favorites(self):
        url = reverse("pet:favorite", kwargs={"pk": self.pet.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_remove_from_favorites(self):
        url = reverse("pet:favorite", kwargs={"pk": self.pet.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedUserTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.db_user = User.objects.create_user(
            email="test@test.com", password="<PASSWORD>"
        )
        self.pet = Pet.objects.create(name="test", pet_type="cat")
        self.token = Token.objects.create(user=self.db_user)
        self.client.force_authenticate(self.db_user, token=self.token.key)

    def test_pets_list(self):
        response = self.client.get(reverse("pet:pets-list"))
        self.assertEqual(status.HTTP_200_OK, response.status_code), "for all users"

    def test_get_pet(self):
        response = self.client.get(
            reverse("pet:pet-detail", kwargs={"pk": self.pet.pk})
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code), "for all users"

    def test_create_pet(self):
        response = self.client.post(
            reverse("pet:pets-list"), data={"name": "Tom", "pet_type": "cat"}
        )
        self.assertEqual(
            status.HTTP_403_FORBIDDEN, response.status_code
        ), "for staff only"

    def test_patch_pet(self):
        response = self.client.patch(
            reverse("pet:pet-detail", kwargs={"pk": self.pet.pk}),
            data={"nae": "newName"},
        )
        self.assertEqual(
            status.HTTP_403_FORBIDDEN, response.status_code
        ), "Endpoint for staff only"

    def test_delete_user(self):
        response = self.client.delete(
            reverse("pet:pet-detail", kwargs={"pk": self.pet.pk})
        )
        self.assertEqual(
            status.HTTP_403_FORBIDDEN, response.status_code
        ), "Endpoint for staff only"

    def test_upload_image(self):
        url = reverse("pet:pet-upload-image", kwargs={"pk": self.pet.pk})
        response = self.client.post(url)
        self.assertEqual(
            status.HTTP_403_FORBIDDEN, response.status_code
        ), "Endpoint for staff only"

    def test_add_to_favorites(self):
        url = reverse("pet:favorite", kwargs={"pk": self.pet.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_remove_from_favorites(self):
        url = reverse("pet:favorite", kwargs={"pk": self.pet.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class StaffUserTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.db_user = User.objects.create_user(
            email="test@test.com", password="<PASSWORD>", is_staff=True
        )
        self.pet = Pet.objects.create(name="test", pet_type="cat")
        self.token = Token.objects.create(user=self.db_user)
        self.client.force_authenticate(self.db_user, token=self.token.key)

    def test_pets_list(self):
        response = self.client.get(reverse("pet:pets-list"))
        self.assertEqual(status.HTTP_200_OK, response.status_code), "for all users"

    def test_get_pet(self):
        response = self.client.get(
            reverse("pet:pet-detail", kwargs={"pk": self.pet.pk})
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code), "for all users"

    def test_create_pet(self):
        response = self.client.post(
            reverse("pet:pets-list"), data={"name": "Tom", "pet_type": "cat"}
        )
        self.assertEqual(
            status.HTTP_201_CREATED, response.status_code
        ), "for staff only"

    def test_patch_pet(self):
        response = self.client.patch(
            reverse("pet:pet-detail", kwargs={"pk": self.pet.pk}),
            data={"nae": "newName"},
        )
        self.assertEqual(
            status.HTTP_200_OK, response.status_code
        ), "Endpoint for staff only"

    def test_delete_pet(self):
        response = self.client.delete(
            reverse("pet:pet-detail", kwargs={"pk": self.pet.pk})
        )
        self.assertEqual(
            status.HTTP_204_NO_CONTENT, response.status_code
        ), "Endpoint for staff only"

    def test_upload_image(self):
        test_file = SimpleUploadedFile(
            "test.jpg", b"file_content_here", content_type="image/jpeg"
        )
        url = reverse("pet:pet-upload-image", kwargs={"pk": self.pet.pk})
        response = self.client.post(url, {"file": test_file}, format="multipart")
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code),
        self.assertEqual(
            [
                "Upload a valid image. The file you uploaded was either not an image or a corrupted image."
            ],
            response.json().get("file"),
        )

    def test_add_to_favorites(self):
        url = reverse("pet:favorite", kwargs={"pk": self.pet.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_remove_from_favorites(self):
        url = reverse("pet:favorite", kwargs={"pk": self.pet.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # @pytest.mark.container
    # def test_upload_image_in_docker(self):
    #     test_file = SimpleUploadedFile(
    #         "test.jpg",
    #         b"file_content_here",
    #         content_type="image/jpeg"
    #     )
    #     url = reverse("pet:pet-upload-image", kwargs={"pk": self.pet.pk})
    #     response = self.client.post(
    #         url,
    #         {"file": test_file},
    #         format='multipart'
    #     )
    #     print(response.json())
    #     self.assertEqual(
    #         status.HTTP_201_CREATED,
    #         response.status_code
    #     )
