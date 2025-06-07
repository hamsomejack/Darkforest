import socket
import json


def connect(host: str, port: int) -> socket.socket:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    return sock


def listen(host: str, port: int, backlog: int = 5) -> socket.socket:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(backlog)
    return server


def reliable_send(sock: socket.socket, data):
    jsondata = json.dumps(data)
    sock.send(jsondata.encode())


def reliable_recv(sock: socket.socket):
    data = ''
    while True:
        try:
            data += sock.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue
