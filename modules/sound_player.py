import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame

class SoundPlayer:
    def __init__(self):
        pygame.mixer.init()

    def play(self, file_path: str):
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

