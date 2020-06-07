from backend.utils.graphql.mutation_type import mutation
from backend.utils.redis_client.redis_client import redis_client
from validator_collection import is_url
from urllib.parse import urlparse
from backend.utils.celery.celery import call_scraper
from starlette.background import BackgroundTask
from backend.scraper.scraper_lib.main import scrape
import time
import asyncio


@mutation.field("initiateTest")
async def initiate_test(object, info, url: str):
    start = time.perf_counter()
    redis_client.delete('allsites:queue')
    if not is_url(url):
        return "INVALID_URL"
    netloc = urlparse(url).netloc
    if netloc.startswith('www.'):
        netloc = netloc.lstrip('www.')
    if redis_client.sismember("siteblacklist", netloc) == 1:
        return "BLACKLIST"
    if redis_client.sismember('allsites:queue', netloc) == 1:
        return "CURRENTLY_QUEUED"
    else:
        # https://github.com/encode/starlette/issues/769
        # bg_tasks.add(asyncio.coroutine(ctx.redis.set), page_id, page)
        call_scraper(url, netloc)
        end = time.perf_counter() - start
        print(f'took {end} seconds')
        return "SUCCESS"

# https://www.ariadnegraphql.org/docs/enums
