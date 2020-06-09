from .redis_client import redis_client
from os import getcwd, path
from more_itertools import chunked


# Load words from a txt file into a set
def load_words(file: str):
    with open(file) as word_file:
        valid_words = set(word_file.read().lower().split())
    return valid_words


def seed_redis(override=False):
    values = redis_client.scard('dict:all')

    if values < 1500000 or override:
        redis_client.delete('dict:all')
        # all_english_words = load_words(
        #     path.join(getcwd(), "./backend/utils/data/wlist_match2.txt")).union(
        #     load_words(path.join(getcwd(), "./backend/utils/data/wlist_match1.txt")).union(
        #         load_words(path.join(getcwd(), "./backend/utils/data/personal_whitelist.txt"))))
        all_english_words = load_words(
            path.join(getcwd(), "./backend/utils/data/wlist_match2.txt")).union(
            load_words(path.join(getcwd(), "./backend/utils/data/wlist_match1.txt")).union(
                load_words(path.join(getcwd(), "./backend/utils/data/personal_whitelist.txt"))))
        chunks = list(chunked(all_english_words, 10000))
        for chunk in chunks:
            redis_client.sadd('dict:all', *chunk)
    return redis_client.scard('dict:all')


def seed_redis_site_blacklist(override=False):
    from backend.celery_worker import hello
    print('----------------------------------------------------------------------------')
    values = redis_client.scard('siteblacklist')
    if values < 2000 or override:
        all_sites = load_words(path.join(getcwd(), "./backend/utils/data/wlist_match2.txt"))
        redis_client.sadd('siteblacklist', *list(all_sites))
    return redis_client.scard('siteblacklist')
