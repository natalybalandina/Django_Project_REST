from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from users.models import Payment, User
from users.serializer import PaymentSerializers, UserSerializer


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializers
    queryset = Payment.objects.all()
    filter_backends = [
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]  # Добавляем DjangoFilterBackend
    filterset_fields = ["payment_course", "payment_lesson", "payment_method"]
    ordering_fields = ["payment_date"]