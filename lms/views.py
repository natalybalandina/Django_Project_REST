from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics, permissions, filters, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend

from lms.models import Course, Lesson, Subscription, Payment
from lms.serializer import (
    CourseSerializer, LessonSerializer, SubscriptionSerializer,
    CourseWithSubscriptionSerializer, PaymentSerializer, PaymentCreateSerializer
)
from lms.permissions import CoursePermissions, LessonPermissions
from lms.paginators import LessonPagination, CoursePagination
from lms.services import StripeService
from users.permissions import IsModerator

User = get_user_model()


class CourseViewSet(viewsets.ModelViewSet):
    """ViewSet для управления курсами"""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated, CoursePermissions]
    pagination_class = CoursePagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['owner']
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'name']

    def get_serializer_class(self):
        return CourseWithSubscriptionSerializer if self.action == 'retrieve' else CourseSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or IsModerator().has_permission(self.request, self):
            return Course.objects.all()
        return Course.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['get'])
    def subscription_status(self, request, pk=None):
        course = self.get_object()
        is_subscribed = course.subscriptions.filter(user=request.user).exists()
        return Response({'course': course.name, 'is_subscribed': is_subscribed})


class LessonViewSet(viewsets.ModelViewSet):
    """ViewSet для управления уроками"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated, LessonPermissions]
    pagination_class = LessonPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['course', 'owner']
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'name']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or IsModerator().has_permission(self.request, self):
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SubscriptionAPIView(APIView):
    """API для управления подписками на курсы"""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        course_id = request.data.get('course_id')

        if not course_id:
            return Response({'error': 'Не указан ID курса'}, status=status.HTTP_400_BAD_REQUEST)

        course = get_object_or_404(Course, id=course_id)
        subscription = Subscription.objects.filter(user=user, course=course)

        if subscription.exists():
            subscription.delete()
            message = 'Подписка удалена'
        else:
            Subscription.objects.create(user=user, course=course)
            message = 'Подписка добавлена'

        return Response({
            'message': message,
            'course_id': course_id,
            'course_name': course.name,
            'is_subscribed': not subscription.exists()
        }, status=status.HTTP_200_OK)

    def get(self, request):
        subscriptions = Subscription.objects.filter(user=request.user)
        serializer = SubscriptionSerializer(subscriptions, many=True)
        return Response(serializer.data)


class PaymentViewSet(viewsets.ModelViewSet):
    """ViewSet для управления платежами"""

    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = PaymentCreateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        payment = serializer.save()
        return Response(PaymentSerializer(payment).data, status=status.HTTP_201_CREATED)


class PaymentStatusAPIView(APIView):
    """Проверка статуса платежа"""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        session_id = request.query_params.get('session_id')

        if not session_id:
            return Response({'error': 'session_id обязателен'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            payment = Payment.objects.get(stripe_session_id=session_id, user=request.user)
            payment_status, session_status = StripeService.get_session_status(session_id)

            if payment_status == 'paid' and payment.status != 'succeeded':
                payment.status = 'succeeded'
                payment.save()

            return Response({
                'payment_status': payment_status,
                'session_status': session_status,
                'payment_id': payment.id,
                'course_id': payment.course.id if payment.course else None,
                'amount': payment.amount
            })

        except Payment.DoesNotExist:
            return Response({'error': 'Платеж не найден'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PaymentSuccessAPIView(APIView):
    """Страница успешной оплаты (для редиректа из Stripe)"""

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        session_id = request.GET.get('session_id')

        if session_id:
            try:
                payment = Payment.objects.get(stripe_session_id=session_id)
                if payment.status != 'succeeded':
                    payment_status, _ = StripeService.get_session_status(session_id)
                    if payment_status == 'paid':
                        payment.status = 'succeeded'
                        payment.save()

                return Response({
                    'message': 'Оплата прошла успешно!',
                    'payment_id': payment.id,
                    'course': payment.course.name if payment.course else None,
                    'amount': payment.amount
                })
            except Payment.DoesNotExist:
                pass

        return Response({'message': 'Оплата прошла успешно!'})


class PaymentCancelAPIView(APIView):
    """Страница отмены оплаты (для редиректа из Stripe)"""

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response({'message': 'Оплата отменена. Вы можете попробовать снова.'})