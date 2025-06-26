from django.urls import path
from pet.views import PetViewSet, FavoriteView, filter_report

app_name = "pet"

pets_list_create = PetViewSet.as_view(actions={"get": "list", "post": "create"})
pet_detail = PetViewSet.as_view(
    actions={"get": "retrieve", "patch": "partial_update", "delete": "destroy"}
)
pet_upload_image = PetViewSet.as_view(actions={"post": "upload_image"})

urlpatterns = [
    path("favorite/<int:pk>/", FavoriteView.as_view(), name="favorite"),
    path("filters/", filter_report, name="filters"),
    path(
        "<int:pk>/upload/", pet_upload_image, name="pet-upload-image"
    ),  # Доданий маршрут для upload
    path("<int:pk>/", pet_detail, name="pet-detail"),
    path("", pets_list_create, name="pets-list"),
]
