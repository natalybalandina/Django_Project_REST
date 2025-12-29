from users.models import Payment, User
from rest_framework import serializers


class PaymentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    payments = PaymentSerializers(many=True, read_only=True)  # Добавляем историю платежей

    class Meta:
        model = User
        fields = '__all__'  # Включаем поле payments