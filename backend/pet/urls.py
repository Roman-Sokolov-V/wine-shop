from django.urls import path
from pet.views import PetViewSet

app_name = "pet"

pets_list_create = PetViewSet.as_view(actions={"get": "list", "post": "create"})
pet_detail = PetViewSet.as_view(
    actions={
        "get": "retrieve",
        "put": "update",
        "patch": "partial_update",
        "delete": "destroy"
    }
)

urlpatterns = [
    path("", pets_list_create, name="pets_list_create"),
    path("<int:pk>/", pet_detail, name="pet_detail"),
]
