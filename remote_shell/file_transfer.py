import socket

def upload(sock: socket.socket, file_path: str):
    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(1024)
            if not chunk:
                break
            sock.send(chunk)


def download(sock: socket.socket, file_path: str):
    with open(file_path, 'wb') as f:
        sock.settimeout(1)
        try:
            while True:
                chunk = sock.recv(1024)
                if not chunk:
                    break
                f.write(chunk)
        except socket.timeout:
            pass
        finally:
            sock.settimeout(None)
