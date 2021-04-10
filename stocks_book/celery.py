import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stocks_book.settings')

app = Celery('stocks_book')

#  all celery-related configuration keys should have a `CELERY_` prefix
app.config_from_object('django.conf:settings', namespace='CELERY')

# get bhavcopy only on weekdays. Markets are closed on weekends
app.conf.beat_schedule = {
    'get_bhav_copy_at_18': {
        'task': 'stocks.tasks.get_bhav_copy',
        'schedule': crontab(hour=18, minute=0, day_of_week='1-5')
    }
}

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
