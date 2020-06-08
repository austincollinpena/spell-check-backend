from backend.utils.celery.not_celery import app
import asyncio
from backend.scraper.scraper_lib.main import scrape


# TODO: Celery forget! check the keys
@app.task
def call_scraper(url, netloc):
    asyncio.ensure_future(scrape(url, netloc))
