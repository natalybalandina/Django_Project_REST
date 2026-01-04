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


class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]
