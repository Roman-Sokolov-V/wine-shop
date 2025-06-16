from django.urls import path
from rest_framework.authtoken import views
from backend.user.views import UserViewSet, LoginView

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
    path("<pk>/", user_detail, name="user-detail"),
    path("", users_list, name="users-list"),

]
urlpatterns += [
    path('api-token-auth/', views.obtain_auth_token)
]