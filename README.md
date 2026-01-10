 # Тестирование
## Запуск тестов

** Запуск всех тестов**
```
python manage.py test
```

**Запуск тестов конкретного приложения**
```
python manage.py test lms.tests
python manage.py test users.tests
```

## Тестирование с покрытием
```
coverage run manage.py test
coverage report
```

## Результаты покрытия тестами
```
ame                                                                               Stmts   Miss  Cover
------------------------------------------------------------------------------------------------------
config\__init__.py                                                                     0      0   100%
config\settings.py                                                                    27      0   100%
config\urls.py                                                                         3      0   100%
lms\__init__.py                                                                        0      0   100%
lms\admin.py                                                                           4      0   100%
lms\apps.py                                                                            4      0   100%
lms\migrations\0001_initial.py                                                         6      0   100%
lms\migrations\0002_alter_course_options_alter_lesson_options_and_more.py              5      0   100%
lms\migrations\0003_alter_course_options_alter_lesson_options_and_more.py              5      0   100%
lms\migrations\0004_course_created_at_course_owner_course_updated_at_and_more.py       7      0   100%
lms\migrations\0005_subscription.py                                                    6      0   100%
lms\migrations\0006_alter_subscription_subscribed_at.py                                5      0   100%
lms\migrations\0007_alter_course_options_alter_lesson_options_and_more.py              4      0   100%
lms\migrations\__init__.py                                                             0      0   100%
lms\models.py                                                                         42      3    93%
lms\paginators.py                                                                      9      0   100%
lms\permissions.py                                                                    19      3    84%
lms\serializer.py                                                                     46      7    85%
lms\tests.py                                                                          95      0   100%
lms\urls.py                                                                            7      0   100%
lms\validators.py                                                                     19      7    63%
lms\views.py                                                                          95     10    89%
manage.py                                                                             11      2    82%
users\__init__.py                                                                      2      1    50%
users\admin.py                                                                         5      0   100%
users\apps.py                                                                          4      0   100%
users\management\__init__.py                                                           0      0   100%
users\management\commands\__init__.py                                                  0      0   100%
users\managers.py                                                                     19      8    58%
users\migrations\0001_initial.py                                                       7      0   100%
users\migrations\0002_remove_user_courses_remove_user_lessons_and_more.py              4      0   100%
users\migrations\0003_alter_user_options_alter_user_managers_and_more.py               7      0   100%
users\migrations\0004_delete_payment.py                                                4      0   100%
users\migrations\__init__.py                                                           0      0   100%
users\models.py                                                                       15      0   100%
users\permissions.py                                                                  13      1    92%
users\serializer.py                                                                   21      0   100%
users\tests.py                                                                        54      0   100%
users\urls.py                                                                          7      0   100%
users\views.py                                                                        48     14    71%
------------------------------------------------------------------------------------------------------
TOTAL                                                                                629     56    91%
```


# Статус проекта
Задание 1: 
 - JWT авторизация - Выполнено
Задание 2:
 - Группа модераторов - Выполнено
Задание 3:
 - Права владельца объектов - Выполнено
Задание 4:
 - Тестирование - Выполнено
Доп. задания:
 - Полное покрытие API - Выполнено

Таким образом, все функциональные требования реализованы и протестированы.
