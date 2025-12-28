from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PaymentViewSet

app_name = 'users'

router = DefaultRouter()

router.register(r'payments', PaymentViewSet)

urlpatterns = [
    path('', include(router.urls)),  # Включаем маршруты из роутера
]