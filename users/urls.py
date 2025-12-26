from django.urls import path

from users.apps import UsersConfig
from users.views import UserListApiView, UserUpdateApiView

app_name = UsersConfig.name

urlpatterns = [
    path("", UserListApiView.as_view(), name="user_list"),
    path("<int:pk>/update/", UserUpdateApiView.as_view(), name="users_update"),
]