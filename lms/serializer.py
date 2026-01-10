from rest_framework import serializers
from lms.models import Course, Lesson, Subscription
from lms.validators import YouTubeURLValidator


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['id', 'user', 'course', 'subscribed_at']
        read_only_fields = ['user', 'subscribed_at']


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        read_only_fields = ['owner']
        validators = [
            YouTubeURLValidator(field='video_url'),
        ]

class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True, source="lesson_set")
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            'id', 'name', 'preview', 'description', 'owner',
            'lesson_count', 'lessons', 'is_subscribed',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['owner', 'is_subscribed']

    def get_lesson_count(self, obj):
        return obj.lesson_set.count()


    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return obj.subscriptions.filter(user=user).exists()
        return False


class CourseWithSubscriptionSerializer(CourseSerializer):
    """Сериализатор курса с детальной информацией о подписке"""
    subscription = serializers.SerializerMethodField()

    class Meta(CourseSerializer.Meta):
        fields = CourseSerializer.Meta.fields + ['subscription']

    def get_subscription(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            subscription = obj.subscriptions.filter(user=user).first()
            if subscription:
                return SubscriptionSerializer(subscription).data
        return None


class CourseDetailSerializer(CourseSerializer):
    """Сериализатор для детального отображения курса"""
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True, source="lesson_set")

    class Meta:
        model = Course
        fields = [
            'name', 'preview', 'description', 'lesson_count', 'lessons'
        ]
