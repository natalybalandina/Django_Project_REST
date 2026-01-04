from rest_framework import serializers
from lms.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        read_only_fields = ['owner']


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True, source="lesson_set")

    class Meta:
        model = Course
        fields = ['id', 'name', 'preview', 'description', 'owner', 'lesson_count', 'lessons', 'created_at', 'updated_at']
        read_only_fields = ['owner']

    def get_lesson_count(self, obj):
        return obj.lesson_set.count()