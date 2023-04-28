import pygame
import pygame.freetype

from src.chess.const import *
pygame.init()

class Home:
    def __init__(self):
        pass


    def show(self, surface):
        surface.fill((80, 80, 80))

        rect_x = 0
        rect_y = 0
        rect_width = 600
        rect_height = 800

        rect = pygame.Rect(rect_x, rect_y, rect_width, rect_height)
        gradient_surf = pygame.Surface((rect_width, rect_height))

        blue = (130, 167, 174)
        green = (152, 206, 184)

        for y in range(rect_height):
            r = blue[0] + (green[0] - blue[0]) * (y / rect_height)
            g = blue[1] + (green[1] - blue[1]) * (y / rect_height)
            b = blue[2] + (green[2] - blue[2]) * (y / rect_height)
            pygame.draw.rect(gradient_surf, (r, g, b), (0, y, rect_width, 1))

        surface.blit(gradient_surf, (rect_x, rect_y), special_flags=pygame.BLEND_RGB_MULT)









