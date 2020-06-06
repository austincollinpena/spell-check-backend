from backend.utils.graphql.mutation_type import mutation
from backend.utils.redis_client.redis_client import redis_client
from validator_collection import is_url
from urllib.parse import urlparse
from starlette.background import BackgroundTask
from backend.scraper.scraper_lib.main import scrape


@mutation.field("initiateTest")
async def initiate_test(object, info, url: str):
    if not is_url(url):
        return "INVALID_URL"
    netloc = urlparse(url).netloc
    if netloc.startswith('www.'):
        netloc = netloc.lstrip('www.')
    if redis_client.sismember("siteblacklist", netloc):
        return "BLACKLIST"
    if redis_client.sismember('allsites:queue', netloc):
        return "CURRENTLY_QUEUED"
    else:
        BackgroundTask(await scrape(url, netloc))
        return "SUCCESS"

# https://www.ariadnegraphql.org/docs/enums
