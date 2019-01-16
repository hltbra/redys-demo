import redis


def get_redis():
    r = redis.StrictRedis('localhost', 6380)
    r.flushall()
    return r


def test_get():
    r = get_redis()
    assert r.get('notfound') is None


def test_set():
    r = get_redis()
    assert r.set("testkey", "testvalue")
    assert r.get("testkey") == "testvalue"


def test_incr():
    r = get_redis()
    assert r.incr('notfound') == 1

    r.set('NaA', 'NaN')
    assert r.incr('NaN') == 1

    r.set('mynumber', 20)
    assert r.incr('mynumber') == 21
    assert r.get('mynumber') == '21'
