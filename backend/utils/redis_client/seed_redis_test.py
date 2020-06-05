import pytest
from .seed_redis import seed_redis, seed_redis_site_blacklist


def test_seed_redis():
    assert seed_redis() > 1500000


def test_seed_blacklist():
    assert seed_redis_site_blacklist() > 2000
