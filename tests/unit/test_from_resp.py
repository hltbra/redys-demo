from redys import from_resp


def test_parse_simple_string():
    result = from_resp("+PING\r\n")
    assert result == [['PING']]


def test_simple_array():
    result = from_resp("*1\r\n$4\r\nPING\r\n")
    assert result == [['PING']]


def test_bulk_string_inside_array():
    result = from_resp("\
*5\r\n\
$4\r\n\
EVAL\r\n\
$69\r\n\
redis.call('set', KEYS[1], KEYS[2])\n\
return redis.call('get', KEYS[1])\r\n\
$1\r\n\
2\r\n\
$7\r\n\
testkey\r\n\
$9\r\n\
testvalue\r\n")

    assert result == [[
        'EVAL',
        '''redis.call('set', KEYS[1], KEYS[2])\nreturn redis.call('get', KEYS[1])''',
        '2',
        'testkey',
        'testvalue'
    ]]


def test_multiple_arrays():
    result = from_resp("*1\r\n$4\r\nPING\r\n*1\r\n$4\r\nPING\r\n")
    assert result == [['PING'], ['PING']]
