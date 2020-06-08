# https://github.com/bstiel/celery-4-windows/blob/master/app.py

# Asyncio integration https://stackoverflow.com/questions/39815771/how-to-combine-celery-with-asyncio
from __future__ import absolute_import, unicode_literals
import asyncio

from celery import Celery
from backend import config

app = Celery('celery_worker',
             broker=config.REDIS_URL)

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    app.start()

# TODO: Celery forget! check the keys
@app.task
def call_scraper(url, netloc):
    asyncio.ensure_future(scrape(url, netloc))