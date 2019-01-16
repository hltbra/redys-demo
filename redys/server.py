import asyncore
import socket

from redys import to_resp, from_resp


def execute_command(cmd_name, *args):
    return 'PONG'


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
