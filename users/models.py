from django.contrib.auth.models import AbstractUser
from django.db import models
from users.managers import CustomUserManager


class User(AbstractUser):
    username = None

    email = models.EmailField(
        unique=True, verbose_name="Почта", help_text="Укажите почту"
    )

    phone = models.CharField(
        max_length=35,
        blank=True,
        null=True,
        verbose_name="Телефон",
        help_text="Укажите телефон",
    )
    city = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Город",
        help_text="Укажите город",
    )
    avatar = models.ImageField(
        upload_to="users/avatars",
        blank=True,
        null=True,
        verbose_name="Аватар",
        help_text="Загрузите аватар",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


# УДАЛИТЕ ВРЕМЕННО модель Payment для создания миграций
# Мы создадим ее позже
# class Payment(models.Model):
#     PAYMENT_OPTIONS = (
#         ("Cash", "Наличные"),
#         ("Non_cash", "Безналичные"),
#     )
#     user = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name="payments",
#         verbose_name="Пользователь",
#     )
#     payment_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата оплаты")
#     payment_course = models.ForeignKey(
#         'lms.Course',
#         on_delete=models.SET_NULL,
#         blank=True,
#         null=True,
#         verbose_name="Оплаченный курс",
#     )
#     payment_lesson = models.ForeignKey(
#         'lms.Lesson',
#         on_delete=models.SET_NULL,
#         blank=True,
#         null=True,
#         verbose_name="Оплаченный урок",
#     )
#     price = models.IntegerField(verbose_name="Сумма оплаты", default=0)
#     payment_method = models.CharField(
#         max_length=50, choices=PAYMENT_OPTIONS, verbose_name="Способ оплаты"
#     )
#
#     class Meta:
#         verbose_name = "Оплата"
#         verbose_name_plural = "Оплаты"