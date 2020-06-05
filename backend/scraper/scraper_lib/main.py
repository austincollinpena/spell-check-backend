import httpx
import asyncio
import aiohttp
from backend.utils.redis_client.redis_client import redis_client
from fake_headers import Headers
from urllib.parse import urlparse
from bs4 import BeautifulSoup

from backend.scraper.scraper_lib.random_proxy import random_proxy
from .get_text import get_text



async def parse_page(redis_client, url: str, session, netloc: str):
    header = Headers()
    async with session.get(url, header=header.generate(), ssl=False, allow_redirects=True,
                           proxy=random_proxy()) as resp:
        if resp.status in [403, 429]:
            number_of_errors = redis_client.hincrby('4xxerrors', url, 1)
            if number_of_errors > 3:
                redis_client.srem(f'active:{netloc}')
        soup = BeautifulSoup(await resp.text(), "html.parser")
        visible_words = get_text(soup)
        wrong_words = await check_if_spelled_right(redis_client, words=visible_words)


async def scrape(url: str):
    assert urlparse(url).netloc == url
    redis_client.sadd(f'active:{url}')  # 1 2
    redis_client.sadd(f'all:{url}')  # 1 2 3 4 5
    redis_client.sadd(f'allsites:queue')

    async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(keepalive_timeout=10, limit=1, verify_ssl=False)) as open_session:
        new_tasks = []

        for active_url in redis_client.smembers(f'active:{url}'):
            task = asyncio.create_task(parse_page(redis_client, active_url.decode('utf-8'), open_session, netloc))
            new_tasks.append(task)
        # Run the initial tasks
        await asyncio.gather(*new_tasks)

# TODO: Sleep for 1 second after getting the content
