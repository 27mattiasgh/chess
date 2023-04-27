import pygame
pygame.init()

class Sound:
    def __init__(self):
        pass

    def play(self, capture, check, mate):
        sound = 'move'

        if capture:
            sound = 'capture'
        if check:
            sound = 'check'
        if mate:
            sound = 'won' if mate == 'won' else 'lost'

        pygame.mixer.Sound(f'assets/sounds/{sound}.wav').play()

