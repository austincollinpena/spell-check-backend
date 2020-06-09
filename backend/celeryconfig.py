from backend import config
from celery import current_app

broker_url = config.REDIS_URL
imports = ('backend.scraper.scraper_lib.main',)
# TODO: Turn this off
celery_always_eager = True
task_ignore_result = True
