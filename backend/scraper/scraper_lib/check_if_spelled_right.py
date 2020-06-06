import re


async def check_if_spelled_right(redis_client, words: list, english_dict: str = "dict:all") -> list:
    wrong_words = []
    for word in words:
        if not redis_client.sismember(english_dict, word) and re.match(
                '^[a-z]*$', word
        ):
            wrong_words.append(word)
    return wrong_words
