# from django.core.management.base import BaseCommand
# from users.models import Payment, User
# from lms.models import Course, Lesson
# from datetime import datetime, timedelta
#
#
# class Command(BaseCommand):
#     help = 'Creates test payment data'
#
#     def handle(self, *args, **options):
#         # Получаем или создаем тестовые данные, если их нет
#         user = User.objects.first()
#         if not user:
#             user = User.objects.create_user(
#                 email='check@yandex.ru',
#                 password='testpass11111'
#             )
#
#         course = Course.objects.first()
#         if not course:
#             course = Course.objects.create(
#                 name='Тестовый курс',
#                 description='Описание тестового курса'
#             )
#
#         lesson = Lesson.objects.first()
#         if not lesson:
#             lesson = Lesson.objects.create(
#                 name='Тестовый урок',
#                 description='Описание тестового урока',
#                 course=course
#             )
#
#         # Создаем платежи
#         #Payment.objects.create(
#             #user=user,
#             #payment_date=datetime.now() - timedelta(days=1),
#             #paid_course=course,
#             #paid_lesson=None,
#             #amount=10000,
#             #payment_method='transfer'
#         #)
#
#         #Payment.objects.create(
#            # user=user,
#            # payment_date=datetime.now(),
#            # paid_course=None,
#            # paid_lesson=lesson,
#            # amount=2000,
#            # payment_method='cash'
#         #)
#
#         #self.stdout.write(self.style.SUCCESS('Successfully created 2 payments'))