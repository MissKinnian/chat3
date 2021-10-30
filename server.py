#!/usr/bin/env python3
"""chatserver server"""

import logging
from argparse import ArgumentParser
from socket import AF_INET, SOCK_STREAM, socket, SOL_SOCKET, SO_REUSEADDR
from threading import Thread

from chatlib import LCG, xor


list_of_clients = []


def client_thread(conn, addr, key):
    """client thread"""

    conn.send(xor('Welcome to this chatroom!', key).encode())

    while True:
        try:
            message = xor(conn.recv(2048).decode(), key)
            if message:
                broadcast(f'<{addr[0]}> {message}', conn, key)
            else:
                break
        except Exception as exc:  # noqa: E722 pylint: disable=broad-except
            logging.error('cannot handle message: %s', exc)
            break

    conn.close()
    remove(conn)


def broadcast(message, from_conn, key):
    """send message to all clients except the original sender"""

    for client in list_of_clients:
        if client != from_conn:
            try:
                client.send(xor(message, key).encode())
            except Exception as exc:  # noqa: E722 pylint: disable=broad-except
                logging.error('cannot broadcast message: %s', exc)
                client.close()
                remove(client)


def remove(conn):
    """remove dead client"""

    if conn in list_of_clients:
        list_of_clients.remove(conn)


def main():
    """main"""

    parser = ArgumentParser()
    parser.add_argument('--bindaddr', default='')
    parser.add_argument('--port', type=int, default=7000)
    args = parser.parse_args()

    key = str(LCG().random())
    server = socket(AF_INET, SOCK_STREAM)
    server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server.bind((args.bindaddr, args.port))
    server.listen(100)

    while True:
        conn, addr = server.accept()
        print(f'{addr[0]} connected')
        list_of_clients.append(conn)
        Thread(target=client_thread, args=(conn, addr, key)).start()

    for conn in list_of_clients:
        conn.close()
    server.close()


if __name__ == '__main__':
    main()
