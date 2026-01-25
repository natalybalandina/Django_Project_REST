import logging
from celery import shared_task
from celery.exceptions import MaxRetriesExceededError
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=300)
def check_inactive_users(self):
    """
    Проверка неактивных пользователей и их блокировка с обработкой ошибок и повторными попытками
    """

    from django.contrib.auth import get_user_model
    User = get_user_model()

    try:
        logger.info("Запуск задачи check_inactive_users")

        month_ago = timezone.now() - timedelta(days=30)

        users_to_warn = User.objects.filter(
            last_login__lt=month_ago,
            is_active=True
        )

        warned_count = users_to_warn.count()
        logger.info(f'Найдено пользователей для предупреждения: {warned_count}')

        warning_sent = 0
        for user in users_to_warn:
            try:
                send_mail(
                    subject='Предупреждение о блокировке аккаунта',
                    message=f'''
                    Здравствуйте, {user.email}!
                    Ваш аккаунт будет заблокирован, т.к. Вы не заходили в систему более месяца. Чтобы избежать блокировки, войдите в систему в ближайшее время.

                    С уважением,
                    Команда LMS-платформы
                    ''',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=True,
                )
                warning_sent += 1
                logger.debug(f'Предупреждение отправлено: {user.email}')

            except Exception as email_error:
                logger.error(f'Ошибка отправки письма {user.email}: {str(email_error)}')

        # Блокируем пользователей, которые не заходили более 33 дней
        users_to_block = User.objects.filter(
            last_login__lt=month_ago - timedelta(days=3),
            is_active=True
        )

        blocked_count = 0
        for user in users_to_block:
            try:
                user.is_active = False
                user.save(update_fields=['is_active'])
                blocked_count += 1
                logger.info(f'Пользователь заблокирован: {user.email}')

            except Exception as block_error:
                logger.error(f'Ошибка блокировки {user.email}: {str(block_error)}')

        result = {
            'status': 'success',
            'warned_users': warned_count,
            'warning_sent': warning_sent,
            'blocked_users': blocked_count,
            'timestamp': timezone.now().isoformat()
        }

        logger.info(f'Задача завершена: {result}')
        return result

    except Exception as exc:
        logger.error(f'Критическая ошибка в задаче check_inactive_users: {str(exc)}')
        try:
            # Повтор через 5 минут
            raise self.retry(exc=exc, countdown=300)
        except MaxRetriesExceededError:
            logger.critical('Превышено максимальное количество попыток для check_inactive_users')
            return {
                'status': 'error',
                'message': f'Ошибка после 3 попыток: {str(exc)}'
            }


@shared_task(bind=True, max_retries=3, default_retry_delay=30)
def send_welcome_email(self, user_id):
    """
    Отправка приветственного письма новому пользователю с повторными попытками при ошибках
    """

    from django.contrib.auth import get_user_model
    User = get_user_model()

    try:
        user = User.objects.get(id=user_id)
        logger.info(f'Отправка приветственного письма для {user.email}')

        send_mail(
            subject='Добро пожаловать в LMS-платформу!',
            message=f'''
            Здравствуйте, {user.first_name or 'пользователь'}!

            Добро пожаловать на нашу образовательную платформу.

            Ваш email: {user.email}
            Дата регистрации: {user.date_joined.strftime("%d.%m.%Y %H:%M")}

            Для начала работы перейдите по ссылке: http://localhost:8000/

            С уважением,
            Команда LMS-платформы
            ''',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )

        logger.info(f'Приветственное письмо успешно отправлено для {user.email}')
        return {
            'status': 'success',
            'message': f'Письмо отправлено для {user.email}',
            'user_id': user_id
        }

    except User.DoesNotExist:
        logger.error(f'Пользователь с id={user_id} не найден')
        # Не повторяем задачу, если пользователя не существует
        return {
            'status': 'error',
            'message': f'Пользователь {user_id} не найден',
            'user_id': user_id
        }

    except Exception as exc:
        logger.error(f'Ошибка при отправке приветственного письма: {str(exc)}')
        try:
            # Повтор через 30 секунд
            raise self.retry(exc=exc, countdown=30)
        except MaxRetriesExceededError:
            logger.critical(f'Превышено количество попыток для приветственного письма {user_id}')
            return {
                'status': 'error',
                'message': f'Ошибка после 3 попыток: {str(exc)}',
                'user_id': user_id
            }