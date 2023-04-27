import pygame
import pygame.freetype

from src.chess.const import *
pygame.init()

class Home:
    def __init__(self):
        pass

    def show(self, surface):
        surface.fill((80, 80, 80))
        font = pygame.font.Font(None, 46)

        pygame.draw.rect(surface, (130, 167, 174), pygame.Rect(0, 0, WINDOW_WIDTH, 180), border_bottom_left_radius=10, border_bottom_right_radius=10) #Title



        pygame.draw.rect(surface, (130, 167, 174), pygame.Rect(25, 230, 512, 300), border_radius=10) #Top Left (Computer)
        
        pygame.draw.rect(surface, (255,156,89), pygame.Rect(25, 555, 512, 300), border_radius=10) #Bottom Left (Puzzles)





        pygame.draw.rect(surface, (130, 167, 174), pygame.Rect(563, 230, 512, 300), border_radius=10) #Top Right
        
        pygame.draw.rect(surface, (130, 167, 174), pygame.Rect(563, 555, 512, 300), border_radius=10) #Bottom Right



        pygame.draw.rect(surface, (100, 100, 100), pygame.Rect(25, 870, 1050, 55), border_radius=10) #Bottom Right



