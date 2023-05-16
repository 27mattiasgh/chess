import pygame
import getpass
from src.chess.const import *

pygame.init()

class Home:
    def __init__(self):
        self.background = pygame.transform.scale(pygame.image.load(r'assets\images\background.png'), (1000, 750))

    def home(self, surface):
        surface.blit(self.background, (0, 0))
        small_font = pygame.font.Font(r"assets\fonts\HelveticaNeueBold.ttf", 24)

        large_font = pygame.font.Font(r"assets\fonts\HelveticaNeueBold.ttf", 40)
        reset_surface = large_font.render(f"Welcome Back {getpass.getuser().split()[0]}!", True, (255, 255, 255))
        surface.blit(reset_surface, (30, 30))

        


        transparent_surface = pygame.Surface((WINDOW_WIDTH - 30, 210), pygame.SRCALPHA)  # Create a transparent surface
        pygame.draw.rect(transparent_surface, (0, 0, 0, 25), pygame.Rect(0, 0, WINDOW_WIDTH - 30, 210), border_radius=10)
        surface.blit(transparent_surface, (15, 15))  # Draw the transparent surface on the main surface




        


        transparent_surface = pygame.Surface((477, 230), pygame.SRCALPHA)
        pygame.draw.rect(transparent_surface, (0, 0, 0, 25), pygame.Rect(0, 0, 477, 230), border_radius=10)
        surface.blit(transparent_surface, (15, 240))
        pygame.draw.rect(surface, (89, 125, 243), pygame.Rect(15, 240, 10, 230), border_top_left_radius=10, border_bottom_left_radius=10)

        text_surface = large_font.render("Online", True, (255, 255, 255))
        transparent_surface = text_surface.convert_alpha()
        transparent_surface.set_alpha(150)
        surface.blit(transparent_surface, (30, 240))
        


        transparent_surface = pygame.Surface((477, 230), pygame.SRCALPHA)
        pygame.draw.rect(transparent_surface, (0, 0, 0, 25), pygame.Rect(0, 0, 477, 230), border_radius=10)
        surface.blit(transparent_surface, (507, 240))
        pygame.draw.rect(surface, (174, 89, 243), pygame.Rect(507, 240, 10, 230), border_top_left_radius=10, border_bottom_left_radius=10)


        


        transparent_surface = pygame.Surface((477, 230), pygame.SRCALPHA)
        pygame.draw.rect(transparent_surface, (0, 0, 0, 25), pygame.Rect(0, 0, 477, 230), border_radius=10)
        surface.blit(transparent_surface, (15, 485))
        pygame.draw.rect(surface, (243, 166, 89), pygame.Rect(15, 485, 10, 230), border_top_left_radius=10, border_bottom_left_radius=10)


        transparent_surface = pygame.Surface((477, 230), pygame.SRCALPHA)
        pygame.draw.rect(transparent_surface, (0, 0, 0, 25), pygame.Rect(0, 0, 477, 230), border_radius=10)
        surface.blit(transparent_surface, (507, 485))
        pygame.draw.rect(surface, (240, 216, 122), pygame.Rect(507, 485, 10, 230), border_top_left_radius=10, border_bottom_left_radius=10)




        

    def settings(self, surface):
        pass

