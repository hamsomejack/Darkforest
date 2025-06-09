<div align="center">
    <a href="https://github.com/kit4py/darkforest/stargazers">
        <img src="https://img.shields.io/github/stars/kit4py/darkforest?color=cba6f7&style=for-the-badge&logo=starship">
    </a>
    <a href="https://github.com/kit4py/darkforest/issues">
        <img src="https://img.shields.io/github/issues/kit4py/darkforest?color=fae3b0&style=for-the-badge&logo=github">
    </a>
    <a href="https://github.com/kit4py/darkforest/network/members">
        <img src="https://img.shields.io/github/forks/kit4py/darkforest?color=94e2d5&style=for-the-badge&logo=git-fork">
    </a>
    <a href="https://github.com/kit4py/darkforest/blob/main/LICENSE">
        <img src="https://img.shields.io/badge/license-MIT-rosewater?color=f5e0dc&style=for-the-badge&logo=archlinux">
    </a>
</div>

# Darkforest

A modular, scalable remote shell toolkit for Linux with session management, keylogging, audio recording, and more (features under development).


## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/kit4py/darkforest.git
   cd darkforest
   ```
2. Install dependencies in editable mode:

   ```bash
   pip install -e .
   ```
3. Ensure system dependencies:

   ```bash
   sudo apt update && sudo apt install ffmpeg
   ```

## Usage

### Start the server (listener)

```bash
rserver --host 0.0.0.0 --port 5555
```

### Launch the client (agent)

```bash
rclient --host <SERVER_IP> --port 5555
```

The client will detach to the background and free your terminal.

## Menu Commands

When the server starts, use the `darkforest>` prompt:

* `sessions`           : List active sessions
* `enter <session_id>` : Interact with a session
* `kill <session_id>`  : Terminate a session
* `clear`              : Clear the screen
* `help`               : Show this help message
* `quit`               : Exit the server

## In-Session Shell Commands

Once inside a session, the prompt changes to:

```
* [<session_id>] Shell~(<client_addr>):
```

Available commands:

* `cd <path>`           : Change directory on client
* `download <file>`     : Download file from client to server
* `upload <file>`       : Upload file from server to client
* `clear`               : Clear this local shell screen
* `exit`                : Return to the main menu
* `quit`                : Close the session

## Feature Modules (under development)

* **Keylogger**: `keylogger_start` / `keylogger_stop` (logs saved as `keylogs_session_<id>.txt`)
* **Privilege Escalation**: `priv_escalate`
* **Microphone Recorder**: `record_mic <seconds>` (MP3/WAV conversion requires `ffmpeg`)
* **Sound Player**: `play_sound <file.mp3>`



## Legal Disclaimer

> You expressly understand and agree that Darkforest (creators and contributors) shall not be liable for any damages or losses resulting from your use of this tool or third-party products that use it.
>
> **Creators have no responsibility for:**
>
> * Unlawful or illegal use of the tool.
> * Legal or law infringement by third parties and users.
> * Acts against ethical and/or human moral, cultural, or societal norms.
> * Malicious use or distribution causing damage to third parties.

---

© 2025 Darkforest Contributors. Licensed under the MIT License.

