from django.db import models


class Course(models.Model):
    """
    Хранит информацию о курсе.

    Связанные модели:
    - :model:`lms.Lesson` - уроки, входящие в этот курс
    """

    name = models.CharField(
        max_length=150, verbose_name="Название курса", help_text="Введите название курса"
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

    def __str__(self):
        return self.name


class Lesson(models.Model):
    """
    Хранит информацию об уроке, входящие в этот курс.

    Связанные модели:
    - :model:`lms.Course` - курс, в который входит урок
    """

    name = models.CharField(
        max_length=50, verbose_name="Название урока", help_text="Введите название урока"
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
        Course, on_delete=models.CASCADE, verbose_name="Курс", help_text="Выберите курс"
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return f"{self.name} (курс: {self.course.name})"
