from django.urls import path
from pet.views import PetViewSet, UploadImageView, AddToFavorite

app_name = "pet"

pets_list_create = PetViewSet.as_view(actions={"get": "list", "post": "create"})
pet_detail = PetViewSet.as_view(
    actions={"get": "retrieve", "patch": "partial_update", "delete": "destroy"}
)

urlpatterns = [
    path("<int:pk>/", pet_detail, name="pet-detail"),
    path("favorite/<int:pk>/", AddToFavorite.as_view(), name="add-to-favorite"),
    path("upload/", UploadImageView.as_view(), name="upload-image"),
    path("", pets_list_create, name="pets-list"),
]
