from backend.utils.graphql.subscription_type import subscription
import asyncio


@subscription.source("counter")
async def counter_generator(obj, info):
    # Entrypoint of the subscription
    for i in range(20):
        await asyncio.sleep(1)
        yield i  # This yields a resoponse that gets sent to the resolver


@subscription.field('counter')
def counter_resolver(count, info):
    return count + 1
