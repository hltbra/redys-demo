from redys import to_resp


def test_integer():
    assert to_resp(1) == ':1\r\n'


def test_nil():
    assert to_resp(None) == '$-1\r\n'


def test_string():
    assert to_resp('test') == '$4\r\ntest\r\n'


def test_array():
    assert to_resp([1, 'two']) == '*2\r\n:1\r\n$3\r\ntwo\r\n'
    assert to_resp([
        [1]
    ]) == '*1\r\n*1\r\n:1\r\n'
