from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView
from users.serializers import UserSerializer
from users.models import User
from rest_framework.permissions import AllowAny


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)  # Сохраняем пароль в хешированном виде
        user.save()


class UserListApiView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserUpdateApiView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'email'


class UserDetailApiView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDeleteApiView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
