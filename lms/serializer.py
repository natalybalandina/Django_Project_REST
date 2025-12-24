from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from lms.models import Course, Lesson

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"

# Включаем все поля модели Course, включая lesson_count
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"

class CourseDetailSerializer(ModelSerializer):
    lesson_count = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True, source="lesson_set")

    def get_lesson_count(self, course):
        """Возвращает количество уроков, связанных с курсом."""
        return course.lesson_set.count()

    class Meta:
        model = Course
        fields = (
            "id",  # Возможно, вы захотите включить идентификатор курса
            "name",
            "preview",
            "description",
            "lesson_count",
            "lessons",
        )