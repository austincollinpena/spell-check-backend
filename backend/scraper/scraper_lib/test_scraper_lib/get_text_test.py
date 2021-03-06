import requests
from fake_headers import Headers
from bs4 import BeautifulSoup
from ..get_text import get_text


def test_get_text():
    header = Headers()
    resp = requests.get("http://example.com/", headers=header.generate())
    soup = BeautifulSoup(resp.text, "html.parser")
    correct_resp = ['Example', 'Domain', 'This', 'domain', 'is', 'for', 'use', 'in', 'illustrative', 'examples', 'in',
                    'documents.', 'You', 'may', 'use', 'this', 'domain', 'in', 'literature', 'without', 'prior',
                    'coordination', 'or', 'asking', 'for', 'permission.', 'More', 'information...']
    assert get_text(soup) == correct_resp
