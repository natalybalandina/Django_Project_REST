from django.contrib.auth.models import AbstractUser
from django.db import models

from lms.models import Course, Lesson


class User(AbstractUser):
    username = None

    email = models.EmailField(
        verbose_name="E-mail", unique=True, help_text="Введите электронную почту"
    )
    phone_number = models.CharField(
        verbose_name="Телефон",
        max_length=20,
        blank=True,
        null=True,
        help_text="Введите номер телефона",
    )
    city = models.CharField(
        verbose_name="Город",
        max_length=50,
        blank=True,
        null=True,
        help_text="Укажите город",
    )
    avatar = models.ImageField(
        verbose_name="Аватар",
        upload_to="users/avatars/",
        blank=True,
        null=True,
        help_text="Загрузите свое фото",
    )

    courses = models.ManyToManyField(Course, blank=True, related_name='students', verbose_name="Курсы", help_text="Выберите курсы")

    lessons = models.ManyToManyField(Lesson, blank=True, related_name='students', verbose_name="Уроки", help_text="Выберите уроки")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["email"]

