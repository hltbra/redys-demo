import asyncore
import socket

from redys import to_resp, from_resp


class Database(object):

    _DB = {}

    def set(self, key, value):
        # with open('/tmp/{}'.format(key), 'w') as f:
        #     f.write(value)
        self._DB[key] = value

    def get(self, key):
        # with open('/tmp/{}'.format(key), 'r') as f:
        #     return f.read()
        return self._DB.get(key)

    def clear(self):
        # return
        self._DB.clear()


DB = Database()


def execute_command(cmd_name, *args):
    if cmd_name.lower() == 'flushall':
        DB.clear()
        return 'OK'
    if cmd_name.lower() == 'get':
        result = DB.get(args[0])
        if result is None:
            return result
        else:
            return str(result)
    if cmd_name.lower() == 'set':
        DB.set(args[0], args[1])
        return 'OK'
    if cmd_name.lower() == 'ping':
        return 'PONG'
    if (
            cmd_name.lower() == 'incr' or
            cmd_name.lower() == 'incrby'
    ):
        current_value = DB.get(args[0])
        try:
            current_value = int(current_value)
        except TypeError:
            current_value = 0
        result = current_value + 1
        DB.set(args[0], result)
        return result
    return '-invalid command'


class CommandHandler(asyncore.dispatcher):

    def handle_read(self):
        data = self.recv(10000)
        print("[debug] data = %r" % data)
        if not data:
            return
        commands = from_resp(data)
        for cmd in commands:
            result = execute_command(*cmd)
            self.send(to_resp(result))


class RedisServer(asyncore.dispatcher):

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(1024)

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            print('Incoming connection from {}'.format(addr))
            CommandHandler(sock)


if __name__ == '__main__':
    RedisServer('0.0.0.0', 6380)

    try:
        print("Running")
        asyncore.loop(use_poll=True)
    except KeyboardInterrupt:
        print("Shutting down...")
