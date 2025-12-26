from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(
        verbose_name="E-mail", unique=True, help_text="Введите электронную почту"
    )
    avatar = models.ImageField(
        verbose_name="Аватар",
        upload_to="users/avatars/",
        blank=True,
        null=True,
        help_text="Загрузите свое фото",
    )
    phone_number = models.CharField(
        verbose_name="Телефон",
        max_length=15,
        blank=True,
        null=True,
        help_text="Введите номер телефона",
    )
    city = models.CharField(
        verbose_name="Город",
        max_length=30,
        blank=True,
        null=True,
        help_text="Укажите город",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["email"]