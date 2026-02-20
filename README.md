# LMS Platform - Платформа онлайн-обучения

Платформа для онлайн-обучения с автоматической системой деплоя, фоновыми задачами через Celery и оплатой через Stripe.

# Адрес сайта (Production)
<http://93.77.180.191>

# О проекте
LMS Platform — это полнофункциональная платформа для онлайн-обучения с возможностью:
- Управления курсами и уроками
- Подписки на обновления курсов
- Оплаты через Stripe
- Автоматической отправки уведомлений
- Фоновых задач через Celery
- Полного CI/CD pipeline

## Запуск проекта через Docker

### Требования
- Docker Engine 20.10+
- Docker Compose 2.0+
- Git
- cоздан файл .env (см. .env_sample)
  
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

## Переменные окружения (.env) на основе .env_sample
```
# Django
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,93.77.180.191

# Database
POSTGRES_DB=lms_db
POSTGRES_USER=lms_user
POSTGRES_PASSWORD=lms_password
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Redis
REDIS_HOST=redis
REDIS_PORT=6379

# Stripe (опционально)
STRIPE_SECRET_KEY=sk_test_dummy
STRIPE_PUBLISHABLE_KEY=pk_test_dummy
```

**Опциональные переменные:**

```
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.yandex.ru
EMAIL_PORT=465
EMAIL_USE_SSL=True
EMAIL_HOST_USER=your-email@yandex.ru
EMAIL_HOST_PASSWORD=your-password
DEFAULT_FROM_EMAIL=your-email@yandex.ru
```
# Деплой и CI/CD
Автоматический деплой
При каждом 'push' в ветки 'develop' или 'feature/homeworke-35.2':
1. Автоматически запускаются тесты
2. После успешных тестов происходит деплой на сервер
3. Обновляется код, применяются миграции, перезапускается Gunicorn

# Настройка сервера
Требования
- Ubuntu 24.04
- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- Nginx
- Gunicorn

## Шаги по развертыванию
**1. Подключение к серверу**
```
ssh bal1nataly@93.77.180.191
```

**2. Установка зависимостей**
```
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip python3-venv nginx git redis-server postgresql postgresql-contrib
```

**3. Настройка базы данных**
```
sudo -u postgres psql -c "CREATE USER lms_user WITH PASSWORD 'lms_password';"
sudo -u postgres psql -c "CREATE DATABASE lms_db OWNER lms_user;"
```

**4. Клонирование проекта**
```
git clone https://github.com/natalybalandina/Django_Project_REST.git
cd Django_Project_REST
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**5. Настройка окружения**
```
cp .env_sample .env
nano .env  # Если нужно отредактируйте под свои параметры
```

**6. Применение миграций**
```
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

**7. Настройка Gunicorn как сервиса**
```
sudo nano /etc/systemd/system/gunicorn.service
```
```
[Unit]
Description=gunicorn daemon for LMS project
After=network.target postgresql.service redis-server.service

[Service]
User=deployer
Group=www-data
WorkingDirectory=/home/deployer/lms_project
Environment="PATH=/home/deployer/lms_project/venv/bin"
EnvironmentFile=/home/deployer/lms_project/.env
ExecStart=/home/deployer/lms_project/venv/bin/gunicorn \
          --access-logfile /home/deployer/lms_project/logs/gunicorn_access.log \
          --error-logfile /home/deployer/lms_project/logs/gunicorn_error.log \
          --workers 3 \
          --bind 127.0.0.1:8000 \
          config.wsgi:application
Restart=always

[Install]
WantedBy=multi-user.target
```

**8. Запуск сервисов**
```
sudo systemctl daemon-reload
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
sudo systemctl start nginx
sudo systemctl enable nginx
```

**9. Настройка фаервола**
```
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw --force enable
```

# GitHub Secrets
Для работы CI/CD необходимо добавить следующие секреты в репозиторий (Settings → Secrets and variables → Actions):

Secret Name	           | Описание
------------------------------------------
SERVER_HOST	           | IP сервера (93.77.180.191)
SERVER_USER	           | Пользователь для деплоя (deployer)
SERVER_SSH_KEY	       | Приватный SSH-ключ для подключения
DJANGO_SECRET_KEY	     | Секретный ключ Django
POSTGRES_DB            |	Имя БД (lms_db)
POSTGRES_USER	         | Пользователь БД (lms_user)
POSTGRES_PASSWORD	     | Пароль БД (lms_password)
POSTGRES_HOST	         | Хост БД (localhost)
POSTGRES_PORT          |	Порт БД (5432)
REDIS_HOST	           | Хост Redis (localhost)
REDIS_PORT             |	Порт Redis (6379)
STRIPE_SECRET_KEY	     | Секретный ключ Stripe
STRIPE_PUBLISHABLE_KEY |	Публичный ключ Stripe
------------------------------------------------


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

# ВЫВОД
Файл 'docker-compose.yaml' полностью покрывает все требования задания:

- Все сервисы описаны (PostgreSQL, Redis, Django, Celery, и др.)

- Правильные порты и зависимости

- Используются переменные окружения из .env

- Есть 'healthcheck' для сервисов

- Все настроено для работы в единой сети
