from celery import Celery
from backend import config

celery_worker = Celery('celery_worker', broker=config.REDIS_URL, include=['backend.scraper.scraper_lib.main', ])

celery_worker.conf.update(
    result_expires=3600
)


@celery_worker.task
def hello():
    return 'hello world!'

# This works: celery -A backend.celery_worker worker --loglevel=info
