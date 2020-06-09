from urllib.parse import urlparse, urljoin
import re
import logging
from . import main
import asyncio


# TODO: test as much as possible here
async def extract_and_queue_local_links(soup, netloc: str, redis_client, session, spell_checker):
    # If there are more than 1000 links to a site, stop scraping
    active_links = redis_client.scard(f'all{netloc}')
    # active_links = int(active_links)
    if active_links >= 1000:
        return

    href_tags = soup.find_all("a", href=True)
    links = [a['href'] for a in href_tags]
    prog = re.compile('http.*(wp-content|.png|.jpg|.jpeg|.svg)')
    valid_links = []
    # parse away query params
    for url in links:
        try:
            valid_links.append(urljoin(url, urlparse(url).path))
        except Exception as e:
            logging.warning(f'Failed at extracting {url}', exc_info=True)
    for link in valid_links:
        # STOP anything from wp-content, .png, .jpg, or others
        parsed_url = urlparse(link)
        # empty strings break stuff
        correct_path = '/' if parsed_url.path == '' else parsed_url.path
        # relative links break stuff
        if link.startswith("/"):
            link = f'http://{netloc}{link}'
        # 1. Only add links from the current domain
        # 2. don't double add
        # 3. don't allow unnecessary extensions
        if urlparse(link).netloc == netloc \
                and not redis_client.sismember(f'all:{netloc}', correct_path) \
                and not prog.match(link):
            print('im gonna add')
            print(link)
            redis_client.sadd(f'all:{netloc}', correct_path)
            await main.parse_page(redis_client, link, session, netloc, spell_checker)
