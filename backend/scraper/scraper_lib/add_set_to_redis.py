from urllib.parse import urlparse
import json


def add_set_to_redis(netloc: str, url: str, visible_words: str, wrong_words_set_clean: set, spell_checker,
                     redis_client):
    """
    I'm sure this function is doing too much... probably should have returned items to add later
    """
    path = urlparse(url).path

    if not wrong_words_set_clean:
        redis_response = {"wrong_word": "None",
                          "context_of_mispelling": "None",
                          "correction": "None"}
        redis_client.publish(f'{netloc}:errors', json.dumps(redis_response))
        return

    for wrong_word in wrong_words_set_clean:
        if wrong_word == "":
            continue
        indices = [i for i, x in enumerate(visible_words) if x == wrong_word]
        # For every time the wrong word shows up...
        for index in indices:
            if index in range(3):
                context_of_mispelling = " ".join(str(x) for x in visible_words[0: 5])
            if index in range(len(visible_words) - 3, len(visible_words)):
                context_of_mispelling = " ".join(str(x) for x in visible_words[index - 5: index])
            else:
                context_of_mispelling = " ".join(str(x) for x in visible_words[index - 4: index + 4])
            redis_response = {"wrong_word": wrong_word,
                              "context_of_mispelling": context_of_mispelling,
                              "correction": spell_checker.correction(wrong_word)}
            redis_client.publish(f'{netloc}:errors', json.dumps(redis_response))