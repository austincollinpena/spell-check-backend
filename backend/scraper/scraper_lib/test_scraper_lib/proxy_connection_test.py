from backend import config
import requests
from fake_headers import Headers


def test_proxy_connection():
    proxies = config.PROXY_LIST.strip('][').split(', ')
    for proxy in proxies:
        header = Headers()
        proxy_sample = {"http": proxy}
        resp = requests.get("http://example.com/", proxies=proxy_sample, headers=header.generate())
        assert resp.status_code == 200
