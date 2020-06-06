from urllib.parse import urlparse
import json


def add_set_to_redis(netloc: str, url: str, visible_words: str, wrong_words_set: set, spell_checker, redis_client):
    """
    I'm sure this function is doing too much... probably should have returned items to add later
    """
    path = urlparse(url).path
    for wrong_word in wrong_words_set:
        if wrong_word == "":
            continue
        indices = [i for i, x in enumerate(visible_words) if x == wrong_word]
        # For every time the wrong word shows up...
        for index in indices:
            if index in range(3):
                context_of_mispelling = " ".join(str(x) for x in visible_words[0: 5])
            else:
                context_of_mispelling = " ".join(str(x) for x in visible_words[index - 4: index + 4])
            # TODO: Strip context of mispelling list to a string
            redis_response = {"wrong_word": wrong_word,
                              "context_of_mispelling": context_of_mispelling,
                              "correction": spell_checker.correction(wrong_word)}
            redis_response
            redis_client.publish(f'{netloc}:errors', json.dumps(redis_response))
