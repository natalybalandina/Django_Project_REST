from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

app = Celery('config')

app.config_from_object('django.conf:settings', namespace='CELERY')

#Настройка для работы с Windows
if app.conf.broker_url.startswith('filesystem://'):
    from pathlib import Path

    data_folder = Path('celery/data')
    processed_folder = Path('celery/processed')
    results_folder = Path('celery/results')

    data_folder.mkdir(parents=True, exist_ok=True)
    processed_folder.mkdir(parents=True, exist_ok=True)
    results_folder.mkdir(parents=True, exist_ok=True)

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'check-inactive-users-daily': {
        'task': 'users.tasks.check_inactive_users',
        'schedule': crontab(hour=0, minute=0),  # Ежедневно в полночь
    },
}


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')