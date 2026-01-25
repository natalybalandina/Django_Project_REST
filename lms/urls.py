from django.urls import path, include
from rest_framework.routers import DefaultRouter
from lms.views import (
    CourseViewSet, LessonViewSet, SubscriptionAPIView,
    PaymentViewSet, PaymentStatusAPIView, PaymentSuccessAPIView, PaymentCancelAPIView,
)
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

app_name = 'lms'

router = DefaultRouter()
router.register(r'courses', CourseViewSet)
router.register(r'lessons', LessonViewSet)
router.register(r'payments', PaymentViewSet, basename='payment')

schema_view = get_schema_view(
   openapi.Info(
      title="LMS Platform API",
      default_version='v1.0',
      description="API для платформы онлайн-обучения",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', include(router.urls)),
    path('subscriptions/', SubscriptionAPIView.as_view(), name='subscriptions'),
    path('payments/status/', PaymentStatusAPIView.as_view(), name='payment-status'),
    path('payments/success/', PaymentSuccessAPIView.as_view(), name='payment-success'),
    path('payments/cancel/', PaymentCancelAPIView.as_view(), name='payment-cancel'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]