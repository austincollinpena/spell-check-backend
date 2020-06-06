from backend.utils.redis_client.seed_redis import load_words
from os import path, getcwd
from backend.utils.redis_client.redis_client import redis_client
from backend.utils.redis_client.seed_redis import seed_redis
import re
from more_itertools import chunked
from spellchecker import SpellChecker


def check_if_spelled_right_test():
    seed_redis()
    if redis_client.scard('mispelledwords') < 35000:
        wrong_words = load_words(
            path.join(getcwd(), "./backend/scraper/scraper_lib/test_scraper_lib/some_incorrect_words.txt"))
        chunks = list(chunked(wrong_words, 10000))
        print('adding words in')
        for chunk in chunks:
            redis_client.sadd('mispelledwords', *chunk)
    # len = redis_client.sdiff('dict:all', 'mispelledwords')
    # wrong_words = [word.lower() for word in wrong_words]
    # missed = []
    # for word in wrong_words:
    #     if redis_client.sismember("dict:all", word) and re.match('^[a-z]*$', word):
    #         missed.append(word)
    assert len(redis_client.sinter('dict:all', 'mispelledwords')) == 0


def check_if_spelled_right_test_new_lib():
    spell = SpellChecker()
    wrong_words = load_words(
        path.join(getcwd(), "./backend/scraper/scraper_lib/test_scraper_lib/some_incorrect_words.txt"))
    wrong_words = [word.lower() for word in wrong_words]
    found = spell.unknown(wrong_words)
    return not_found
