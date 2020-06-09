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

    if values < 230000 or override:
        redis_client.delete('dict:all')
        added_words = load_words(
            path.join(getcwd(), "./backend/utils/data/these_words_are_right.txt"))
        chunks = list(chunked(added_words, 10000))
        for chunk in chunks:
            redis_client.sadd('dict:all', *chunk)
    return redis_client.scard('dict:all')


def seed_redis_site_blacklist(override=False):
    print('----------------------------------------------------------------------------')
    values = redis_client.scard('siteblacklist')
    if values < 2000 or override:
        all_sites = load_words(path.join(getcwd(), "./backend/utils/data/site_blacklist.txt"))
        redis_client.sadd('siteblacklist', *list(all_sites))
    return redis_client.scard('siteblacklist')
