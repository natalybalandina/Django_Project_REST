from django.contrib.auth import get_user_model
from .serializer import UserCreateSerializer, UserProfileSerializer, UserPublicSerializer
from rest_framework import viewsets, generics, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .permissions import IsModerator, IsProfileOwner

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

    @action(detail=False, methods=['get', 'put', 'patch'])
    def me(self, request):
        serializer = UserProfileSerializer(request.user, data=request.data,
                                           partial=True)
        if request.method in ['PUT', 'PATCH']:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        return Response(serializer.data)


# Добавьте эти классы для совместимости
class UserRegistrationAPIView(generics.CreateAPIView):
    """API для регистрации пользователя"""
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.AllowAny]


class UserCreateAPIView(generics.CreateAPIView):
    """API для создания пользователя (для обратной совместимости)"""
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.AllowAny]


class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    """API для просмотра и обновления профиля пользователя"""
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class CustomTokenObtainPairView(TokenObtainPairView):
    """Кастомный View для получения JWT токена"""
    permission_classes = [permissions.AllowAny]