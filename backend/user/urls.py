from django.urls import path
from user.views import UserViewSet, LoginView, LogoutView, MeView

app_name = "user"

user_create = UserViewSet.as_view(actions={"post": "create"})
users_list = UserViewSet.as_view(actions={"get": "list"})
user_detail = UserViewSet.as_view(
            actions={
                "get": "retrieve",
                "delete": "destroy",
                "patch": "partial_update"
            }
        )

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("register/", user_create, name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("me/", MeView.as_view(), name="me"),
    path("<pk>/", user_detail, name="user-detail"),
    path("", users_list, name="users-list"),
]
