from .celery import app as celery_app
from stocks.tasks import get_bhav_copy

__all__ = ['celery_app']

get_bhav_copy()