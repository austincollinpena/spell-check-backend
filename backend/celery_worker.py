from celery import Celery
from backend import config

celery_worker = Celery('celery_worker', broker=config.REDIS_URL)


@celery_worker.task
def hello():
    return 'hello world!'

# This works: celery -A backend.celery_worker worker --loglevel=info
