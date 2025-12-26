from django.db import models


class Course(models.Model):
    """Описание модели Курса"""

    title = models.CharField(
        max_length=250, verbose_name="наименование", help_text="Введите название курса", default='Без названия'
    )
    description = models.TextField(
        verbose_name="описание",
        blank=True,
        null=True,
        help_text="Введите описание курса",
    )
    image = models.ImageField(
        verbose_name="изображение",
        blank=True,
        null=True,
        help_text="Загрузите изображение курса",
        upload_to="uploads/",
    )

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ["title"]


class Lesson(models.Model):
    """Описание модели Урока"""

    title = models.CharField(
        max_length=250, verbose_name="наименование", help_text="Введите название урока",  default=''
    )
    description = models.TextField(
        verbose_name="описание",
        blank=True,
        null=True,
        help_text="Введите описание курса",
    )
    image = models.ImageField(
        verbose_name="изображение",
        blank=True,
        null=True,
        help_text="Загрузите изображение курса",
        upload_to="uploads/",
    )
    video = models.CharField(
        verbose_name="ссылка на видео",
        blank=True,
        null=True,
        help_text="Введите ссылку на видео курса",
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="course", verbose_name="курс"
    )

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ["title"]