from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

import pet
from pet.models import Pet

User = get_user_model()


def check_response(instance, pet, data):
    for key, value in data.items():
        instance.assertEqual(pet[key], value), f"pet.{key} should by equal {value}"
    instance.assertIsNotNone(pet["id"])
    instance.assertEqual(pet["images"], [])
    instance.assertEqual(pet["owner"], None)


class StaffUserTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.db_user = User.objects.create_user(
            email="test@test.com", password="<PASSWORD>", is_staff=True
        )
        self.pet_data = {
            "name": "Nora",
            "pet_type": "cat",
            "age": 2,
            "breed": "siam",
            "sex": "F",
            "coloration": "white",
            "weight": 2,
            "is_sterilized": True,
            "description": "it is a monster",
        }
        self.pet = Pet.objects.create(**self.pet_data)
        self.token = Token.objects.create(user=self.db_user)
        self.client.force_authenticate(self.db_user, token=self.token.key)

    def test_pets_list(self):
        response = self.client.get(reverse("pet:pets-list"))
        self.assertEqual(status.HTTP_200_OK, response.status_code),

        for pet in response.json():
            check_response(self, pet, self.pet_data)

    def test_get_pet(self):
        response = self.client.get(
            reverse("pet:pet-detail", kwargs={"pk": self.pet.pk})
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code), "for all users"
        pet = response.json()
        check_response(self, pet, self.pet_data)

    def test_create_pet(self):
        data = {
            "name": "Kesha",
            "pet_type": "dog",
            "age": 2,
            "breed": "pudel",
            "sex": "M",
            "coloration": "black",
            "weight": 4,
            "is_sterilized": False,
            "description": "it is a good boy",
        }
        response = self.client.post(reverse("pet:pets-list"), data=data)
        self.assertEqual(
            status.HTTP_201_CREATED, response.status_code
        ), "for staff only"
        pet = response.json()
        check_response(self, pet, data)

    def test_patch_pet(self):
        new_name = "New Name"
        response = self.client.patch(
            reverse("pet:pet-detail", kwargs={"pk": self.pet.pk}),
            data={"name": new_name},
        )
        self.assertEqual(
            status.HTTP_200_OK, response.status_code
        ), "Endpoint for staff only"
        pet = response.json()
        data = self.pet_data.copy()
        data["name"] = new_name
        check_response(self, pet, data)

    def test_add_to_favorites(self):
        url = reverse("pet:favorite", kwargs={"pk": self.pet.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.pet, self.db_user.favorites.all())

    def test_add_to_favorites_twice(self):
        url = reverse("pet:favorite", kwargs={"pk": self.pet.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.pet, self.db_user.favorites.all())
        url = reverse("pet:favorite", kwargs={"pk": self.pet.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.pet, self.db_user.favorites.all())
