from django.urls import path
from users.apps import UsersConfig
from users.views import UserCreateAPIView, UserListApiView, UserUpdateApiView, UserDetailApiView, UserDeleteApiView

app_name = UsersConfig.name

urlpatterns = [
    path("", UserListApiView.as_view(), name="user_list"),  # Получение списка пользователей
    path("<int:pk>/", UserDetailApiView.as_view(), name="user_detail"),  # Получение одной сущности
    path("create/", UserCreateAPIView.as_view(), name="user_create"),  # Создание нового пользователя
    path("<int:pk>/update/", UserUpdateApiView.as_view(), name="user_update"),  # Изменение пользователя
    path("<int:pk>/delete/", UserDeleteApiView.as_view(), name="user_delete"),  # Удаление пользователя
]