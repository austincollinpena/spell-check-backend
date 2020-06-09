from urllib.parse import urlparse
import json
import re


# TODO: Test this
def add_set_to_redis(netloc: str, url: str, visible_words: str, wrong_words_set_clean: set, spell_checker,
                     redis_client):
    """
    I'm sure this function is doing too much... probably should have returned items to add later
    """
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
        # the spell checker kind of sucks so I have a few custom validations
        # sometimes it will pass through empty strings
        if wrong_word == "":
            continue
        # We only want to correct numbers
        pattern = re.compile('^[a-zA-Z]*$', re.UNICODE)
        if not pattern.fullmatch(wrong_word):
            continue
        correction = spell_checker.correction(wrong_word)
        # it struggles a lot with plural
        if spell_checker.known([wrong_word.strip('s')]):
            continue
        # catch things like monetize vs monetized
        if spell_checker.known([wrong_word.strip('d')]):
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
            print(f'sending to {netloc}:errors')
            if wrong_word == correction:

                redis_response = {"path": path,
                                  "wrongWord": wrong_word,
                                  "contextOfMispelling": context_of_mispelling,
                                  "correction": "NO_CORRECTION"}
                redis_client.publish(f'{netloc}:errors', json.dumps(redis_response))
                redis_client.lpush(f'{netloc}:errorcount', 1)
            else:
                redis_response = {"path": path,
                                  "wrongWord": wrong_word,
                                  "contextOfMispelling": context_of_mispelling,
                                  "correction": correction}
                redis_client.publish(f'{netloc}:errors', json.dumps(redis_response))
                redis_client.lpush(f'{netloc}:errorcount', 1)
