from urllib.parse import urlparse
import json


# TODO: Test this
def add_set_to_redis(netloc: str, url: str, visible_words: str, wrong_words_set_clean: set, spell_checker,
                     redis_client):
    """
    I'm sure this function is doing too much... probably should have returned items to add later
    """
    print('adding to redis')
    path = urlparse(url).path

    if wrong_words_set_clean in [{''}, {""}]:
        print('no wrong words')
        redis_response = {"path": path,
                          "wrongWord": "None",
                          "contextOfMispelling": "None",
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
            redis_response = {"path": path,
                              "wrongWord": wrong_word,
                              "contextOfMispelling": context_of_mispelling,
                              "correction": spell_checker.correction(wrong_word)}
            redis_client.publish(f'{netloc}:errors', json.dumps(redis_response))
