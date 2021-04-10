import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stocks_book.settings')

app = Celery('stocks_book')

#  all celery-related configuration keys should have a `CELERY_` prefix
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'get_bhav_copy_at_18': {
        'task': 'stocks.tasks.get_bhav_copy',
        'schedule': 30,
        # 'schedule': crontab(hour=18, minute=0)
    }
}

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# CELERYBEAT_SCHEDULE = {
#     # Executes every weekday morning at 7:30 A.M
#     'weekdays': {
#         'task': 'tasks.A',
#         'schedule': crontab(hour=7, minute=30, day_of_week='1-5'),
#         'args': (x1, y1),
#     },
#     # Executes saturday morning at 4:00 A.M
#     'saturday': {
#         'task': 'tasks.B',
#         'schedule': crontab(hour=7, minute=30, day_of_week='sat'),
#         'args': (x1, y1),
#     },
#     # Executes sunday morning at 2:15 A.M
#     'sunday': {
#         'task': 'tasks.A',
#         'schedule': crontab(hour=2, minute=15, day_of_week='sun'),
#         'args': (x2, y2),
#     },
# }