from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta


class Course(models.Model):
    """
    Модель курса с автоматической отправкой уведомлений подписчикам
    """
    name = models.CharField(
        max_length=50,
        verbose_name="Название курса",
        help_text="Введите название курса",
    )
    preview = models.ImageField(upload_to="lms/preview_course", blank=True, null=True)
    description = models.TextField(
        verbose_name="Описание курса",
        help_text="Введите описание курса",
        blank=True,
        null=True,
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='courses',
        verbose_name='Владелец',
        null=True,
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Стоимость курса",
        help_text="Стоимость курса в рублях"
    )
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата создания")
    updated_at = models.DateTimeField(default=timezone.now, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Метод для отправки уведомлений  при обновлении курса (если не обновлялся более 4 часов)
        """
        is_new = self.pk is None
        need_send_notification = False
        notification_type = "обновлен"

        if not is_new:
            # Получаем старую версию курса
            old_course = Course.objects.get(pk=self.pk)
            time_diff = timezone.now() - old_course.updated_at

            self.updated_at = timezone.now()

            # Отправляем уведомления только если курс не обновлялся более 4 часов
            if time_diff > timedelta(hours=4):
                need_send_notification = True
        else:
            self.updated_at = timezone.now()

        super().save(*args, **kwargs)

        if need_send_notification:

            from lms.tasks import send_course_update_email
            send_course_update_email.delay(self.pk, notification_type)
            print(f"Задача на отправку уведомлений о курсе {self.pk} добавлена в очередь Celery")


class Lesson(models.Model):
    """
    Модель с автоматической отправкой уведомлений подписчикам курса
    """
    name = models.CharField(
        max_length=50,
        verbose_name="Название урока",
        help_text="Введите название урока",
    )
    preview = models.ImageField(upload_to="lms/preview_lesson", blank=True, null=True)
    description = models.TextField(
        verbose_name="Описание урока",
        help_text="Введите описание урока",
        blank=True,
        null=True,
    )
    video_url = models.URLField(
        verbose_name="Ссылка на видео",
        help_text="Введите ссылку на видеоурок",
        blank=True,
        null=True,
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="Курс",
        help_text="Выберите курс",
        related_name='lessons'
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name='Владелец',
        null=True,
    )
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата создания")
    updated_at = models.DateTimeField(default=timezone.now, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} (курс: {self.course.name})"

    def save(self, *args, **kwargs):
        """
        Метод для отправки уведомлений при создании или обновлении урока
        """
        is_new = self.pk is None
        need_send_notification = False
        notification_type = ""

        if not is_new:
            # Получаем старый объект урока для сравнения
            old_lesson = Lesson.objects.get(pk=self.pk)

            # Проверяем, изменились ли данные урока
            lesson_changed = (
                    self.name != old_lesson.name or
                    self.description != old_lesson.description or
                    self.video_url != old_lesson.video_url or
                    self.course_id != old_lesson.course_id
            )

            if lesson_changed:
                # Проверка обновления курса за последние 4 часа
                course_update_time_diff = timezone.now() - self.course.updated_at

                if course_update_time_diff > timedelta(hours=4):
                    need_send_notification = True
                    notification_type = f"обновлен (изменен урок: {self.name})"
        else:
            # Для нового урока проверяем обновление курса
            course_update_time_diff = timezone.now() - self.course.updated_at

            if course_update_time_diff > timedelta(hours=4):
                need_send_notification = True
                notification_type = f"обновлен (добавлен новый урок: {self.name})"

        self.updated_at = timezone.now()
        super().save(*args, **kwargs)

        # Обновляем дату курса при создании нового урока
        if is_new:
            self.course.updated_at = timezone.now()
            self.course.save(update_fields=['updated_at'])

        # Отправляем уведомление после сохранения
        if need_send_notification:

            from lms.tasks import send_course_update_email
            send_course_update_email.delay(self.course.pk, notification_type)
            print(f"Задача на отправку уведомлений об уроке {self.pk} добавлена в очередь Celery")


class Subscription(models.Model):
    """
    Модель подписки пользователя на курс
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='Пользователь'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='Курс'
    )
    subscribed_at = models.DateTimeField(default=timezone.now, verbose_name='Дата подписки')
    is_active = models.BooleanField(default=True, verbose_name='Активна')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        unique_together = ['user', 'course']
        ordering = ['-subscribed_at']

    def __str__(self):
        status = "активна" if self.is_active else "неактивна"
        return f'{self.user.email} подписан на {self.course.name} ({status})'

    def save(self, *args, **kwargs):
        """
        Метод для отправки приветственного письма при подписке
        """
        is_new = self.pk is None

        super().save(*args, **kwargs)

        # Отправляем уведомление о новой подписке
        if is_new and self.is_active:

            from lms.tasks import send_course_update_email
            send_course_update_email.delay(
                self.course.pk,
                f"новый подписчик: {self.user.email}"
            )
            print(f"Уведомление о новой подписке {self.user.email} на курс {self.course.name}")


class Payment(models.Model):
    """
    Модель платежа за курс
    """
    STATUS_CHOICES = [
        ('pending', 'Ожидает оплаты'),
        ('processing', 'В обработке'),
        ('succeeded', 'Оплачено'),
        ('canceled', 'Отменено'),
        ('failed', 'Не удалось'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('stripe', 'Stripe'),
        ('bank_transfer', 'Банковский перевод'),
        ('cash', 'Наличные'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name='Пользователь'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name='Курс',
        null=True,
        blank=True
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name='Урок',
        null=True,
        blank=True
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Сумма оплаты'
    )
    stripe_product_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='ID продукта в Stripe'
    )
    stripe_price_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='ID цены в Stripe'
    )
    stripe_session_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='ID сессии в Stripe'
    )
    payment_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name='Ссылка для оплаты'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Статус платежа'
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default='stripe',
        verbose_name='Способ оплаты'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    paid_at = models.DateTimeField(null=True, blank=True, verbose_name='Дата оплаты')

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
        ordering = ['-created_at']

    def __str__(self):
        if self.course:
            item = f'за курс "{self.course.name}"'
        elif self.lesson:
            item = f'за урок "{self.lesson.name}"'
        else:
            item = ''
        return f'Платеж #{self.id} - {self.user.email} - {self.amount} руб. {item}'

    def save(self, *args, **kwargs):
        """
        Модель для отправки уведомлений при успешной оплате
        """
        is_new = self.pk is None

        super().save(*args, **kwargs)

        # Отправляем уведомление об успешной оплате
        if not is_new:
            old_payment = Payment.objects.get(pk=self.pk)

            if old_payment.status != 'succeeded' and self.status == 'succeeded':
                self.paid_at = timezone.now()
                self.save(update_fields=['paid_at'])

                if self.course:

                    from lms.tasks import send_course_update_email
                    send_course_update_email.delay(
                        self.course.pk,
                        f"оплачен пользователем {self.user.email}"
                    )
                    print(f"Уведомление об оплате курса {self.course.name}")

    def send_payment_notification(self):
        """
        Отправляет уведомление о платеже
        """

        from lms.tasks import send_course_update_email

        if self.course:
            send_course_update_email.delay(
                self.course.pk,
                f"новый платеж от {self.user.email}: {self.amount} руб."
            )
        return True