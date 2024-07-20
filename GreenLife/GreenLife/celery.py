from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GreenLife.settings')

app = Celery('GreenLife')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'check-schedules-every-day': {
        'task': 'your_app.tasks.check_schedules',
        'schedule': crontab(hour=0, minute=0),  # Runs every day at midnight
    },
}
