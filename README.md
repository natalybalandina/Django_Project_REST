# LMS Platform - Docker Deployment

Проект платформы онлайн-обучения с использованием Docker и Docker Compose.

## Запуск проекта

### Требования
- Docker Engine 20.10+
- Docker Compose 2.0+
- Git
- cоздан файл .env

### Запуск контейнеров
```
docker-compose up -d --build
```

### Проверка работы сервисов

```
docker-compose ps
```

### Остановка контейнеров

```
docker-compose down
```

### Просмотр логов
- Все логи
```
docker-compose logs -f
```

- Логи конкретного сервиса
```
docker-compose logs -f backend
docker-compose logs -f celery_worker
docker-compose logs -f celery_beat
```

## Сервисы и порты
### Работающие сервисы:

- Django Backend: http://localhost:8000
- PostgreSQL: localhost:5432
- Redis: localhost:6379

### API Endpoints:
 -API Documentation: http://localhost:8000/swagger/

- Redoc Documentation: http://localhost:8000/redoc/

- Admin Panel: http://localhost:8000/admin/

- API Base URL: http://localhost:8000/api/

*Учетные данные по умолчанию:*

Суперпользователь: admin@yandex.ru / admin
База данных: lms_db / lms_user / lms_password

*Проверка работоспособности*
**Проверка Django:**
```
 python manage.py runserver
```
 В поисковой строке вводим
```
http://localhost:8000/api/courses/
```
**Проверка Celery Worker:**

```
docker-compose exec backend python manage.py shell -c "from config.celery import app; print(app.control.ping())"
```

**Проверка Celery Beat:**
```
docker-compose exec celery_beat celery -A config beat --loglevel=info --dry-run
```

**Проверка Redis:**

```
docker-compose exec redis redis-cli ping
```

**Проверка PostgreSQL:**
```
docker-compose exec db psql -U lms_user -d lms_db -c "\l"
```

## Переменные окружения (.env)

SECRET_KEY - секретный ключ Django

POSTGRES_* - настройки PostgreSQL

STRIPE_* - ключи Stripe для оплаты

**Опциональные переменные:**

EMAIL_* - настройки email для отправки писем

DEBUG - режим отладки (True/False)

Мониторинг
Статус сервисов:
```
docker-compose ps
```

### Остановить и удалить контейнеры

```
docker-compose down -v
```

### Очистить неиспользуемые образы
```
docker system prune -a
```
