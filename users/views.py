from django.contrib.auth import get_user_model
from .serializer import UserCreateSerializer, UserProfileSerializer, UserPublicSerializer
from rest_framework import viewsets, generics, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .permissions import IsModerator, IsProfileOwner
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action in ['retrieve', 'list']:
            return UserPublicSerializer
        return UserProfileSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        elif self.action == 'list':
            return [permissions.IsAuthenticated(), IsModerator()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsProfileOwner()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        # Для модераторов показываем всех пользователей
        if IsModerator().has_permission(self.request, self):
            return User.objects.all()
        # Обычные пользователи не видят список пользователей
        return User.objects.none()

    @action(detail=False, methods=['get', 'put', 'patch'])
    def me(self, request):
        if request.method in ['PUT', 'PATCH']:
            serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)


class UserRegistrationAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="Регистрация нового пользователя",
        request_body=UserCreateSerializer,
        responses={
            201: UserCreateSerializer,
            400: 'Неверные данные (email уже существует и т.д.)'
        }
    )

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="Получить JWT токен для авторизации",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'password'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email пользователя'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Пароль', format='password'),
            }
        ),
        responses={
            200: openapi.Response(
                description="Токены доступа",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'access': openapi.Schema(type=openapi.TYPE_STRING, description='Access токен'),
                        'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='Refresh токен'),
                    }
                )
            ),
            401: 'Неверные учетные данные'
        }
    )

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
