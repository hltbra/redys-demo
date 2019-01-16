import redis


def get_redis():
    return redis.StrictRedis('localhost', 6379)


def test_ping():
    r = get_redis()
    assert r.ping()  # the redis client compares the output to "PONG" and returns a boolean


def test_get():
    r = get_redis()
    assert r.get('notfound') is None


def test_set():
    r = get_redis()
    assert r.set("testkey", "testvalue")
    assert r.get("testkey") == "testvalue"
