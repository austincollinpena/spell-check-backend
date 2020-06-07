from ..random_proxy import random_proxy


def test_random_proxy():
    for _ in range(20):
        assert 24 < len(random_proxy()) < 28
        assert random_proxy().startswith('http://')
