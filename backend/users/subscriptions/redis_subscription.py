from backend.utils.graphql.subscription_type import subscription
from backend.utils.redis_client.redis_client import redis_client
import asyncio


# TODO: stream_timeout
@subscription.source('redis')
async def redis_generator(obj, info):
    p = redis_client.pubsub()
    p.subscribe('test')
    while True:
        message = p.get_message()
        await asyncio.sleep(.1)
        if message is not None and type(message['data']) == bytes:
            yield message['data'].decode('utf8')


@subscription.field('redis')
def message_resolver(message, info):
    return message
