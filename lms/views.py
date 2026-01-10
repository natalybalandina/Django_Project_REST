from lms.models import Course, Lesson, Subscription
from lms.serializer import CourseSerializer, LessonSerializer, SubscriptionSerializer, CourseWithSubscriptionSerializer
from users.permissions import IsModerator
from rest_framework import viewsets, generics, permissions, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from lms.permissions import CoursePermissions, LessonPermissions
from lms.validators import YouTubeURLValidator
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from lms.paginators import LessonPagination, CoursePagination
from django.contrib.auth import get_user_model


User = get_user_model()


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated, CoursePermissions]
    pagination_class = CoursePagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['owner']
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'name']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CourseWithSubscriptionSerializer
        return CourseSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or IsModerator().has_permission(self.request, self):
            return Course.objects.all()
        return Course.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonViewSet(viewsets.ModelViewSet):
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
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course_id')

        if not course_id:
            return Response(
                {'error': 'Не указан ID курса'},
                status=status.HTTP_400_BAD_REQUEST
            )

        course = get_object_or_404(Course, id=course_id)
        subscription = Subscription.objects.filter(user=user, course=course)

        if subscription.exists():
            subscription.delete()
            message = 'Подписка удалена'
        else:
            Subscription.objects.create(user=user, course=course)
            message = 'Подписка добавлена'

        return Response(
            {
                'message': message,
                'course_id': course_id,
                'course_name': course.name,
                'is_subscribed': not subscription.exists()
            },
            status=status.HTTP_200_OK
        )

    def get(self, request, *args, **kwargs):
        user = request.user
        subscriptions = Subscription.objects.filter(user=user)
        serializer = SubscriptionSerializer(subscriptions, many=True)
        return Response(serializer.data)


class CourseCreateAPIView(generics.CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonCreateAPIView(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CourseListAPIView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CoursePagination


class LessonListAPIView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = LessonPagination