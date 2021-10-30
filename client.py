#!/usr/bin/env python3
"""chatserver client"""

import sys
from argparse import ArgumentParser
from select import select
from socket import AF_INET, SOCK_STREAM, socket

from chatlib import LCG, xor


def main():
    """main"""

    parser = ArgumentParser()
    parser.add_argument('--server', default='chatserver')
    parser.add_argument('--port', type=int, default=7000)
    args = parser.parse_args()

    key = str(LCG().random())
    conn = socket(AF_INET, SOCK_STREAM)
    conn.connect((args.server, args.port))

    while True:
        sockets_list = [sys.stdin, conn]
        read_sockets, _, _ = select(sockets_list, [], [])
        for sock in read_sockets:
            if sock == conn:
                message = xor(sock.recv(2048).decode(), key)
                if message:
                    print(message)
            elif sock == sys.stdin:
                message = sys.stdin.readline().strip()
                conn.send(xor(message, key).encode())
                print(f'<You>{message}')
            else:
                raise RuntimeError('invalid socket to be processed')

    conn.close()


if __name__ == '__main__':
    main()
