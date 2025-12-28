from rest_framework import serializers

from lms.models import Course, Lesson
from rest_framework.fields import SerializerMethodField

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    lesson_count = SerializerMethodField()  # Добавляем поле для количества уроков

    @staticmethod
    def get_lesson_count(course):
        return course.lesson_set.count()

    class Meta:
        model = Course
        fields = "__all__"

class CourseDetailSerializer(serializers.ModelSerializer):
    lesson_count = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True, source="lesson_set")

    @staticmethod
    def get_lesson_count(course):
        return course.lesson_set.count()

    class Meta:
        model = Course
        fields = ("name", "preview", "description", "lesson_count", "lessons")  # Включаем поле lessons