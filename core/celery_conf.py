from celery import Celery
from core.config import settings
import time
import datetime

celery_app = Celery('worker', broker=settings.CELERY_BROKER_URL, backend=settings.CELERY_BACKEND_URL)

#celery beat
celery_app.conf.update(
    time_zone='Asia/Tehran', 
    beat_schedule={
        "print_every_30_seconds": { 
            "task": 'core.celery_conf.print_hello',
            "schedule": 30.0 
        }
    }
)

@celery_app.task
def add_number(x, y):
    return x + y

@celery_app.task
def print_hello():
    now = datetime.datetime.now().strftime('%Y-%m-%d, %H:%M:%S')
    print(f'hello current time : {now}')
    