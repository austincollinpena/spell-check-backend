from __future__ import absolute_import, unicode_literals

from celery import Celery
from backend import config
from backend.scraper.scraper_lib.main import scrape

celery_worker = Celery('celery_worker', broker=config.REDIS_URL, include=['backend.scraper.main'])

celery_worker.conf.update(
    result_expires=3600
)


@celery_worker.task
def hello():
    return 'hello world!'

# This works: celery -A backend.utils.celery_worker_module.celery_worker worker --loglevel=info --pool=solo
