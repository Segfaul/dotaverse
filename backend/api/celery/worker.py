import os

from celery import Celery
from celery.schedules import crontab

celery = Celery(__name__, broker=os.environ['CELERY_BROKER_URL'], include=['backend.api.celery.tasks'])

celery.conf.beat_schedule = {
    'parse_dota-every-70': {
        'task': 'backend.api.celery.tasks.parse_opendota',
        'schedule': crontab(minute='*/70'),
        'args': ()
    },
    'populate_db-every-30': {
        'task': 'backend.api.celery.tasks.populate_db',
        'schedule': crontab(minute='*/30'),
        'args': ()
    },
}
