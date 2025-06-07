import sounddevice as sd
import wavio
import os
import subprocess

class MicRecorder:
    def __init__(self, fs=44100):
        self.fs = fs
        self.recording = None

    def record(self, duration):
        self.recording = sd.rec(int(duration * self.fs), samplerate=self.fs, channels=2)
        sd.wait()

    def save(self, file_path):
        base, ext = os.path.splitext(file_path)
        wav_path = base + '.wav'
        # first write .wav
        wavio.write(wav_path, self.recording, self.fs, sampwidth=2)
        # for .mp3 convert with ffmpeg
        if ext.lower() == '.mp3':
            subprocess.run([
                'ffmpeg', '-y', '-i', wav_path, '-codec:a', 'libmp3lame', '-qscale:a', '2', file_path
            ], check=True)
            os.remove(wav_path)
        else:
            # keep WAV if no mp3
            if wav_path != file_path:
                os.replace(wav_path, file_path)

