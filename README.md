 # Проект содержит:
- Управление курсами и уроками
- Создана модель (пользователи, модераторы, администраторы)
- Реализованы асинхронные email-уведомления через Celery
- Выполняются периодические задачи (т.е. блокировка неактивных пользователей)
- Осуществлена интеграция с Stripe для оплаты курсов
- JWT-аутентификация
- REST API с Swagger документацией
- Осуществлена интеграция с Yandex почтой
- Реализована поддержка Windows и Linux.

  # Установка и запуск
 ## 1. Предварительные требования
 Python 3.13+
 PostgreSQL 15+
 Redis 7+
 Git

 ## 2. Настройка виртуального окружения
 ```
 python -m venv venv
 venv\Scripts\activate
```

## 3. Установка зависимостей
```
pip install -r requirements.txt
```

# Миграции
```
python manage.py migrate
```

# Создание суперпользователя
```
python manage.py createsuperuser
```

# Основные эндпоинты
```
Метод	Эндпоинт	Описание
GET	/api/courses/	Список курсов
POST	/api/courses/	Создание курса
GET	/api/courses/{id}/	Детали курса
PUT	/api/courses/{id}/	Обновление курса
DELETE	/api/courses/{id}/	Удаление курса
POST	/api/subscriptions/	Подписка/отписка от курса
POST	/api/payments/	Создание платежа
GET	/api/payments/status/	Статус платежа
```

# Email уведомления
Система автоматически отправляет уведомления:
- При обновлении курса (если не обновлялся более 4 часов)
- При добавлении нового урока
- При подписке на курс
- При успешной оплате курса

# Периодические задачи
Блокировка неактивных пользователей:
Ежедневно в полночь
Блокирует пользователей, не заходивших более месяца
Отправляет предупреждение за 3 дня до блокировки

# Отчет по тестам
```
coverage run --source='.' manage.py test
```
```
Found 19 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
AUTHENTICATED RESPONSE: 200
.UNAUTHENTICATED RESPONSE: 401
.CREATE COURSE RESPONSE: 201
.COURSES LIST RESPONSE: 200
.CREATE RESPONSE: 201 - {'id': 2, 'name': 'Новый урок', 'preview': None, 'description': 'Описание нового урока', 'video_url': 'https://www.youtube.com/watch?v=abc123', 'created_at': '2026-01-25T22:19:39.722684+03:00', 'updated_at': '2026-01-25T22:19:39.722712+03:00', 'course': 4, 'owner': 4}
.DETAIL RESPONSE: 200
.LIST RESPONSE: 200 - Results: 1
.UPDATE RESPONSE: 200 - {'id': 5, 'name': 'Обновленное название урока', 'preview': None, 'description': 'Описание урока', 'video_url': 'https://www.youtube.com/watch?v=test123', 'created_at': '2026-01-25T22:19:41.028013+03:00', 'updated_at': '2026-01-25T22:19:41.040226+03:00', 'course': 7, 'owner': 7}
.Уведомление о новой подписке test@example.com на курс Курс для подписки
SUBSCRIBE RESPONSE: 200 - {'message': 'Подписка добавлена', 'course_id': 8, 'course_name': 'Курс для подписки', 'is_subscribed': False}
.Уведомление о новой подписке test@example.com на курс Курс для подписки
UNSUBSCRIBE RESPONSE: 200 - {'message': 'Подписка удалена', 'course_id': 9, 'course_name': 'Курс для подписки', 'is_subscribed': True}
.SHORT YOUTUBE RESPONSE: 201
.VALID YOUTUBE RESPONSE: 201
........
----------------------------------------------------------------------
Ran 19 tests in 12.949s

OK
```

```
coverage report
```

```
Name                                                   Stmts   Miss  Cover
--------------------------------------------------------------------------
config\__init__.py                                         2      0   100%
config\asgi.py                                             4      4     0%
config\celery.py                                          22      8    64%
config\settings.py                                        48      0   100%
config\urls.py                                             7      0   100%
config\wsgi.py                                             4      4     0%
lms\__init__.py                                            0      0   100%
lms\admin.py                                              10      0   100%
lms\apps.py                                                4      0   100%
lms\management\__init__.py                                 0      0   100%
lms\management\commands\__init__.py                        0      0   100%
lms\management\commands\test_stripe.py                    27     18    33%
lms\migrations\0001_initial.py                             8      0   100%
lms\migrations\0002_add_is_active_to_subscription.py       5      0   100%
lms\migrations\__init__.py                                 0      0   100%
lms\models.py                                            138     36    74%
lms\paginators.py                                          9      0   100%
lms\permissions.py                                        19      3    84%
lms\serializer.py                                         66     20    70%
lms\services.py                                           59     44    25%
lms\tasks.py                                              46     36    22%
lms\tests.py                                              95      0   100%
lms\urls.py                                               13      0   100%
lms\validators.py                                         19      7    63%
lms\views.py                                             119     42    65%
manage.py                                                 11      2    82%
users\__init__.py                                          2      1    50%
users\admin.py                                             5      0   100%
users\apps.py                                              4      0   100%
users\management\__init__.py                               0      0   100%
users\management\commands\__init__.py                      0      0   100%
users\management\commands\create_groups.py                22     22     0%
users\management\commands\create_payments.py               0      0   100%
users\management\commands\create_superuser.py             10     10     0%
users\managers.py                                         19      8    58%
users\migrations\0001_initial.py                           7      0   100%
users\migrations\__init__.py                               0      0   100%
users\models.py                                           15      0   100%
users\permissions.py                                      13      1    92%
users\serializer.py                                       21      0   100%
users\tasks.py                                            66     66     0%
users\tests.py                                            54      0   100%
users\urls.py                                              8      0   100%
users\views.py                                            56     14    75%
--------------------------------------------------------------------------
TOTAL                                                   1037    346    67%
```

Таким образом, платформа готова к работе
