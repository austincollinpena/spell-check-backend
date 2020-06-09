from celery import Celery
from backend import config
from backend import celeryconfig

celery_worker = Celery()
celery_worker.config_from_object(celeryconfig)


@celery_worker.task
def hello():
    return 'hello world!'

# This works: celery -A backend.celery_worker worker --loglevel=info --pool=solo
# This works: celery -A backend.celery_worker worker --loglevel=info -P solo --without-gossip --without-mingle --without-heartbeat
