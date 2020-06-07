from backend.utils.graphql.subscription_type import subscription
import asyncio
from backend.utils.redis_client.redis_client import redis_client
from urllib.parse import urlparse


@subscription.source('spellingError')
async def spelling_error_generator(obj, info, website):
    p = redis_client.pubsub()
    a = urlparse(website).netloc
    # p.subscribe(f'{a}:errors')
    # For debugging
    p.subscribe(f'debug')
    while True:
        message = p.get_message()
        await asyncio.sleep(.1)
        if message is not None and type(message['data']) == bytes:
            yield message['data'].decode('utf8')


@subscription.field('spellingError')
def spelling_error_resolver(message, info, website):
    return message
