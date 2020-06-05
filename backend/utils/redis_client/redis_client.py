# Using hiredis which uses C bindindings
from redis import Redis
from backend import config

# TODO: keep alive?
redis_client = Redis(host=config.REDIS_HOST,
                     port=config.REDIS_PORT,
                     db=0,
                     ssl_cert_reqs=config.REDIS_SSL,
                     password=str(config.REDIS_PASSWORD),
                     socket_connect_timeout=10)
