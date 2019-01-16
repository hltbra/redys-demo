class Buffer(object):

    CRLF = '\r\n'

    def __init__(self, data):
        self._data = data
        self._index = 0

    def empty(self):
        return len(self._data[self._index:]) == 0

    def advance(self, size):
        start = self._index
        stop = start + size
        result = self._data[start:stop]
        self._index = stop
        return result

    def advance_to_crlf(self):
        crlf = self._index + self._data[self._index:].find(self.CRLF)
        start = self._index
        stop = crlf
        self._index = stop + 2
        return self._data[start:stop]

    def __repr__(self):
        return self._data[self._index:]


def from_resp(data):
    result = []
    buf = Buffer(data)
    while not buf.empty():
        msg_type = buf.advance(1)

        if msg_type == '+':
            command = buf.advance_to_crlf()
            result.append([command])
        elif msg_type == '*':
            cmd_size = buf.advance_to_crlf()
            subresult = []
            for _ in range(int(cmd_size)):
                buf.advance(1)  # skip '$'
                msg_size = buf.advance_to_crlf()
                subresult.append(buf.advance(int(msg_size)))
                buf.advance_to_crlf()
            result.append(subresult)
        else:
            raise TypeError("invalid message %r" % data)

    return result


def to_resp(data):
    result = []

    def _to_resp(elem):
        if elem is None:
            result.append('$-1\r\n')
        elif isinstance(elem, int):
            result.append(':{}\r\n'.format(elem))
        elif isinstance(elem, basestring):
            result.append('${}\r\n{}\r\n'.format(len(elem), elem))
        elif isinstance(elem, list):
            result.append('*{}\r\n'.format(len(elem)))
            for e in elem:
                _to_resp(e)
        else:
            result.append("-ERROR: cant figure out type of {}\r\n".format(repr(elem)))

    _to_resp(data)
    return ''.join(result)
