from sqlalchemy.engine.url import URL, make_url
from starlette.config import Config
from starlette.datastructures import Secret
import os

config = Config("backend/.env")
# try:
#     config('MIGRATION_URL')
# except:
#     config = Config(".env")

MIGRATION_URL = config("MIGRATION_URL", default="You forgot the migration url")

DB_DRIVER = config("DB_DRIVER", default="asyncpg")
DB_HOST = config("DB_HOST", default=None)
DB_PORT = config("DB_PORT", cast=int, default=None)
DB_USER = config("DB_USER", default=None)
DB_PASSWORD = config("DB_PASSWORD", cast=Secret, default=None)
DB_DATABASE = config("DB_DATABASE", default=None)
DB_DSN = config(
    "DB_DSN",
    cast=make_url,
    default=URL(
        drivername=DB_DRIVER,
        username=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_DATABASE,
    ),
)
DB_POOL_MIN_SIZE = config("DB_POOL_MIN_SIZE", cast=int, default=1)
DB_POOL_MAX_SIZE = config("DB_POOL_MAX_SIZE", cast=int, default=16)
DB_ECHO = config("DB_ECHO", cast=bool, default=False)
DB_SSL = config("DB_SSL", default=None)
DB_USE_CONNECTION_FOR_REQUEST = config(
    "DB_USE_CONNECTION_FOR_REQUEST", cast=bool, default=True
)
DB_RETRY_LIMIT = config("DB_RETRY_LIMIT", cast=int, default=1)
DB_RETRY_INTERVAL = config("DB_RETRY_INTERVAL", cast=int, default=1)

SECRET_KEY = config("SECRET_KEY", cast=Secret, default=None)

# Redis

REDIS_SSL = config('REDIS_SSL', default=None)
REDIS_HOST = config('REDIS_HOST', default=None)
REDIS_PORT = config('REDIS_PORT', cast=int, default=None)
REDIS_PASSWORD = config('REDIS_PASSWORD', cast=Secret, default=None)

PROXY_LIST = config('PROXIES', default=None)

REDIS_URL = config('REDIS_URL', default=f'redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}')