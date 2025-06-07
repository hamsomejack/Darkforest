import os
import sys


def escalate_privilege() -> str:
    if os.geteuid() != 0:
        try:
            os.execvp('sudo', ['sudo', sys.executable] + sys.argv)
        except Exception as e:
            return f"[!] Privilege escalation failed: {e}"
    return "[+] Running as root"

