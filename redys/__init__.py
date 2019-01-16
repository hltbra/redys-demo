def from_resp(data):
    return [['PING']]


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
            raise TypeError("cant figure out type of {}".format(repr(elem)))

    _to_resp(data)
    return ''.join(result)
