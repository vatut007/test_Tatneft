import os
from celery import Celery

# Установка модуля настроек Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'metrics.settings')

app = Celery('metrics')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
