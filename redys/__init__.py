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
        first_char = buf.advance(1)
        if first_char == '*':
            subresult = []
            array_length = buf.advance_to_crlf()
            for _ in range(int(array_length)):
                buf.advance(1)
                str_length = buf.advance_to_crlf()
                subresult.append(buf.advance(int(str_length)))
                buf.advance_to_crlf()
            result.append(subresult)
        else:
            result.append([first_char + buf.advance_to_crlf()])
    return result



def to_resp(data):
    result = []
    # simple string
    # errors
    # integers
    # bulk strings
    # arrays
    # nil
    def _to_resp(elem):
        if elem is None:
            result.append('$-1\r\n')
        elif isinstance(elem, int):
            result.append(':{}\r\n'.format(elem))
        elif isinstance(elem, basestring):
            result.append('${}\r\n{}\r\n'.format(len(elem), elem))
        elif isinstance(elem, list):
            elem_length = len(elem)
            result.append('*{}\r\n'.format(elem_length))
            for e in elem:
                _to_resp(e)
        else:
            result.append('-unknown type')
    _to_resp(data)
    return ''.join(result)

