import redis


def get_redis():
    r = redis.StrictRedis('localhost', 6380)
    r.flushall()
    return r


def test_ping():
    r = get_redis()
    assert r.ping()  # the redis client compares the output to "PONG" and returns a boolean
