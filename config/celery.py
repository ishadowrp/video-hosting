import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
 
app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'action_every_day_8am': {
        'task': 'comments_and_chats.tasks.notifications_email_sending',
        'schedule': crontab(hour=8, minute=0),
    },
}

app.autodiscover_tasks()
