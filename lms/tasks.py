import logging
from celery import shared_task
from celery.exceptions import MaxRetriesExceededError
from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_course_update_email(self, course_id, update_type="обновлен"):
    """
    Отправка email подписчикам об обновлении курса с повторными попытками при ошибках
    """

    from lms.models import Subscription, Course

    try:
        logger.info(f'Начинаю отправку уведомлений для курса {course_id}')

        course = Course.objects.get(id=course_id)
        subscribers = Subscription.objects.filter(
            course=course,
            is_active=True
        ).select_related('user')

        subject = f'Курс {update_type}: {course.name}'
        message = f'''
        Здравствуйте!

        Курс "{course.name}" был {update_type}.

        Посмотреть изменения: http://localhost:8000/api/courses/{course_id}/

        С уважением,
        Команда LMS-платформы
        '''

        recipient_list = [subscriber.user.email for subscriber in subscribers]

        if recipient_list:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=recipient_list,
                fail_silently=False,
            )
            logger.info(f'Успешно отправлено уведомлений: {len(recipient_list)}')
            return {
                'status': 'success',
                'message': f'Отправлено {len(recipient_list)} писем',
                'count': len(recipient_list),
                'course_id': course_id,
                'course_name': course.name
            }
        else:
            logger.warning(f'Нет активных подписчиков для курса {course.name}')
            return {
                'status': 'warning',
                'message': 'Нет активных подписчиков',
                'course_id': course_id,
                'course_name': course.name
            }

    except Course.DoesNotExist:
        logger.error(f'Курс с id={course_id} не найден')
        return {
            'status': 'error',
            'message': f'Курс {course_id} не найден',
            'course_id': course_id
        }

    except Exception as exc:
        logger.error(f'Ошибка при отправке email для курса {course_id}: {str(exc)}')
        try:
            # Повтор задачи
            raise self.retry(exc=exc, countdown=60)
        except MaxRetriesExceededError:
            logger.critical(f'Превышено максимальное количество попыток для курса {course_id}')
            return {
                'status': 'error',
                'message': f'Ошибка после 3 попыток: {str(exc)}',
                'course_id': course_id
            }


@shared_task(bind=True, max_retries=2, default_retry_delay=30)
def send_test_email(self):
    """
    Тестовая задача для проверки отправки email с обработкой ошибок
    """
    try:
        # Проверка настроек email
        if not all([
            settings.EMAIL_HOST,
            settings.EMAIL_HOST_USER,
            settings.DEFAULT_FROM_EMAIL
        ]):
            raise ValueError('Настройки email неполные')

        send_mail(
            subject='Тестовое письмо от LMS',
            message='Это тестовое письмо от вашей LMS-платформы.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.EMAIL_HOST_USER],
            fail_silently=False,
        )

        logger.info('Тестовое письмо успешно отправлено')
        return {
            'status': 'success',
            'message': 'Тестовое письмо отправлено'
        }

    except Exception as exc:
        logger.error(f'Ошибка отправки тестового письма: {str(exc)}')
        try:
            raise self.retry(exc=exc, countdown=30)
        except MaxRetriesExceededError:
            return {
                'status': 'error',
                'message': f'Не удалось отправить тестовое письмо: {str(exc)}'
            }