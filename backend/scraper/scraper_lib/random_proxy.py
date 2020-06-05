import random
from backend import config


def random_proxy() -> str:
    proxies = config.PROXY_LIST.strip('][').split(', ')
    return random.choice(proxies)
