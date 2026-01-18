from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from lms.models import Course
from lms.services import StripeService
from django.test import RequestFactory

User = get_user_model()

class Command(BaseCommand):
    help = 'Тестирование интеграции со Stripe'

    def handle(self, *args, **options):
        # Создаем тестовые данные
        user = User.objects.first()
        course = Course.objects.first()

        if not user or not course:
            self.stdout.write(self.style.ERROR('Не найдены тестовые пользователь или курс'))
            return

        # Устанавливаем цену для курса
        course.price = 1000  # 1000 рублей
        course.save()

        # Создаем запрос
        factory = RequestFactory()
        request = factory.get('/')
        request.user = user

        try:
            # Создаем платеж
            payment = StripeService.create_payment_for_course(course, user, request)

            self.stdout.write(self.style.SUCCESS(f'Платеж создан успешно!'))
            self.stdout.write(f'ID платежа: {payment.id}')
            self.stdout.write(f'Сумма: {payment.amount} руб.')
            self.stdout.write(f'Ссылка для оплаты: {payment.payment_url}')

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка: {str(e)}'))