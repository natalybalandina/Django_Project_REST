from django.db import models


class Course(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name="Название курса",
        help_text="Введите название курса",
        blank=True,
        null=True,
    )
    preview = models.ImageField(upload_to="lms/preview_course", blank=True, null=True)
    description = models.CharField(
        max_length=50,
        verbose_name="Описание курса",
        help_text="Введите описание курса",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"



class Lesson(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name="Название урока",
        help_text="Введите название урока",
        blank=True,
        null=True,
    )
    preview = models.ImageField(upload_to="lms/preview_lesson", blank=True, null=True)
    description = models.CharField(
        max_length=50,
        verbose_name="Описание урока",
        help_text="Введите описание урока",
        blank=True,
        null=True,
    )
    video_url = models.CharField(
        verbose_name="Ссылка на видео",
        help_text="Введите ссылку на видеоурок",
        blank=True,
        null=True,
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="Курс",
        help_text="Выберите курс"
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"