from backend.utils.graphql.mutation_type import mutation
from backend.utils.redis_client.redis_client import redis_client
from validator_collection import is_url
from urllib.parse import urlparse
from backend.scraper.scraper_lib.main import call_scraper, scrape
import time


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
        print('calling scraper')
        call_scraper.delay(url, netloc)
        # await scrape(url, netloc)
        end = time.perf_counter() - start
        print(f'took {end} seconds')
        return "SUCCESS"
