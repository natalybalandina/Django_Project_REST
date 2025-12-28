from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from users.models import Payment
from users.serializer import PaymentSerializers


class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializers
    queryset = Payment.objects.all()
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]  # Добавляем DjangoFilterBackend
    filterset_fields = ['payment_course', 'payment_lesson', 'payment_method']
    ordering_fields = ['payment_date']