# Heavily inspired by https://github.com/encode/broadcaster/blob/master/broadcaster/_backends/redis.py

# Using hiredis which uses C bindindings
import redis
from backend import config

redis_client = redis.Redis(host=config.REDIS_HOST,
                           port=config.REDIS_PORT,
                           db=0,
                           ssl_cert_reqs=config.REDIS_SSL,
                           password=config.REDIS_PASSWORD)
