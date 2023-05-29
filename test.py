import pygame
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Transparent Triangle")


triangle_points = [(400, 100), (200, 500), (600, 500)]

background_color = (255, 255, 255) 
triangle_color = (0, 255, 0, 20)  


transparent_surface = pygame.Surface((width, height), pygame.SRCALPHA)
pygame.draw.polygon(transparent_surface, triangle_color, triangle_points)
screen.blit(transparent_surface, (0, 0))


