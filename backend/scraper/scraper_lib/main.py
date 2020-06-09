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

# from backend.utils.celery_worker_module.celery_worker import celery_worker
from backend.celery_worker import celery_worker
from backend.scraper.scraper_lib.random_proxy import random_proxy
from .get_text import get_text
from backend.utils.redis_client.load_words import load_words
from .add_set_to_redis import add_set_to_redis


async def parse_page(redis_client, url: str, session, netloc: str, spell_checker):
    header = Headers()
    assert spell_checker['pinterest'] == True
    async with session.get(url, headers=header.generate(), ssl=False, allow_redirects=True,
                           proxy=random_proxy()) as resp:
        if resp.status in [403, 429]:
            number_of_errors = redis_client.hincrby('4xxerrors', url, 1)
            if number_of_errors > 3:
                redis_client.srem(f'active:{netloc}')
        soup = BeautifulSoup(await resp.text(), "html.parser")
        visible_words_with_punctuation = get_text(soup)
        # TODO
        pattern = re.compile(r'[\W_]+', re.UNICODE)
        visible_words_strip_punctuation = {pattern.sub('', word) for word in visible_words_with_punctuation}
        wrong_words_set = spell_checker.unknown(visible_words_strip_punctuation)
        # TODO get additional URL's
        wrong_words_set_clean = {word for word in wrong_words_set if not ""}

        add_set_to_redis(netloc, url, visible_words_with_punctuation, wrong_words_set_clean, spell_checker,
                         redis_client)
        # TODO: Pop from allsites:queue eventually
        # TODO: IT not being in the queue is what stops the subscription
        # TODO: Elminate the keys when you're done with them

        await asyncio.sleep(1)


@celery_worker.task
async def scrape(url: str, netloc: str):
    redis_client.sadd(f'active:{netloc}', url)  # 1 2
    redis_client.sadd(f'all:{url}', url)  # 1 2 3 4 5
    # TODO: Re add
    redis_client.sadd(f'allsites:queue', netloc)

    wrong_words = load_words(path.join(getcwd(), "./backend/utils/data/these_words_are_wrong.txt"))
    correct_words = load_words(path.join(getcwd(), "./backend/utils/data/these_words_are_right.txt"))
    spell = SpellChecker()
    spell.word_frequency.load_words([*correct_words])
    spell.word_frequency.remove_words([*wrong_words])
    print('dirty dog im a dirty dog')

    async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(keepalive_timeout=10, limit=1, verify_ssl=False)) as open_session:
        new_tasks = []

        for active_url in redis_client.smembers(f'active:{netloc}'):
            task = asyncio.create_task(
                parse_page(redis_client, active_url.decode('utf-8'), open_session, netloc=netloc,
                           spell_checker=spell))
            # TODO: Why can't I just call create_task? Why do I need ensure future?
            # TODO: what does ensure future return?
            new_tasks.append(task)

        # Run the initial tasks
        await asyncio.gather(*new_tasks)

# TODO: Sleep for 1 second after getting the content
