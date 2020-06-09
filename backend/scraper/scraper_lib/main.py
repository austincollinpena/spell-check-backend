import httpx
import asyncio
import aiohttp
from backend.utils.redis_client.redis_client import redis_client
from fake_headers import Headers
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from spellchecker import SpellChecker
from os import path, getcwd
import re
import json
from celery.contrib import rdb

from backend.celery_worker import celery_worker
from backend.scraper.scraper_lib.random_proxy import random_proxy
from .extract_local_links import extract_and_queue_local_links
from .get_text import get_text
from backend.utils.redis_client.load_words import load_words
from .add_set_to_redis import add_set_to_redis


# Redis Key!
# TODO: set expirations
# allsites:queue - takes a netloc so we don't scrape the same site at the same time
# all:{netloc} path - takes the netloc and the path. Allows us to not rescrape the same page
# processed:{netloc} url - takes the netloc and the url. Basically a progress bar for the user
# {netloc}:errors - takes in a json string of errors
# errorcount:{netloc} - takes in a "1" for each error


async def parse_page(redis_client, url: str, session, netloc: str, spell_checker):
    header = Headers()
    assert spell_checker['pinterest'] == True
    print(f'analyzing {url}')
    async with session.get(url, headers=header.generate(), ssl=False, allow_redirects=True,
                           proxy=random_proxy()) as resp:
        if resp.status in [403, 429]:
            number_of_errors = redis_client.hincrby('4xxerrors', url, 1)
            # TODO: I don't think this is the correct redis location
            if number_of_errors > 3:
                redis_client.srem(f'active:{netloc}')
            return

        soup = BeautifulSoup(await resp.text(), "html.parser")
        visible_words_with_punctuation = get_text(soup)
        pattern = re.compile(r'[\W_]+', re.UNICODE)
        visible_words_strip_punctuation = {pattern.sub('', word) for word in visible_words_with_punctuation}
        wrong_words_set = spell_checker.unknown(visible_words_strip_punctuation)
        wrong_words_set_clean = {word for word in wrong_words_set if not ""}
        add_set_to_redis(netloc, url, visible_words_with_punctuation, wrong_words_set_clean, spell_checker,
                         redis_client)

        redis_client.sadd(f'processed:{netloc}', url)
        # this is essentially a recursive search that recalls parse_page() until all the URL's are done
        await extract_and_queue_local_links(soup, netloc, redis_client, session, spell_checker)


# TODO: be fault tolerant
@celery_worker.task
def call_scraper(url: str, netloc: str):
    asyncio.run(scrape(url, netloc))


async def scrape(url: str, netloc: str):
    # TODO: Change this to a path to avoid re adds
    url_path = urlparse(url).path
    if url_path == "":
        url_path = "/"
    redis_client.sadd(f'all:{netloc}', url_path)
    redis_client.sadd(f'allsites:queue', netloc)

    wrong_words = load_words(path.join(getcwd(), "./backend/utils/data/these_words_are_wrong.txt"))
    correct_words = load_words(path.join(getcwd(), "./backend/utils/data/these_words_are_right.txt"))
    spell = SpellChecker()
    spell.word_frequency.load_words([*correct_words])
    spell.word_frequency.remove_words([*wrong_words])

    async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(keepalive_timeout=10, limit=1, verify_ssl=False)) as open_session:
        
        try:
            task = asyncio.create_task(
                parse_page(redis_client, f"https://{netloc}{url_path}", open_session, netloc=netloc,
                           spell_checker=spell))
            await task
        except Exception as e:
            print('faile on main block')
            print(e)
        print('final block running')
        redis_client.srem('allsites:queue', netloc)
        print('im deleting EVERYTHING')
        redis_client.delete(f'all:{netloc}')
# TODO: Sleep for 1 second after getting the content
