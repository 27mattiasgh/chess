
import re
import pygame
import getpass
import datetime
from src.chess.const import *

pygame.init()
mega_font  = pygame.font.Font(r"assets\fonts\HelveticaNeueBold.ttf", 70)
large_font = pygame.font.Font(r"assets\fonts\HelveticaNeueBold.ttf", 40)
medium_font = pygame.font.Font(r"assets\fonts\HelveticaNeueBold.ttf", 18)

class Home:
    def __init__(self):
        self.background = pygame.transform.scale(pygame.image.load(r'assets\images\background.png'), (1000, 750))

    def home(self, surface):

        surface.blit(self.background, (0, 0))

        hour = datetime.datetime.now().hour
        greeting = "Good Morning" if 5 <= hour < 12 else "Good Afternoon" if 12 <= hour < 18 else "Good Evening"
        username = getpass.getuser().split()[0]
        username_letters_only = re.sub(r'[^A-Za-z]', '', username).title()
        reset_surface = mega_font.render(f"{greeting}, {username_letters_only}!", True, (255, 255, 255))

        text_x = (WINDOW_WIDTH - reset_surface.get_width()) // 2
        text_y = (210 - reset_surface.get_height()) // 2  
        surface.blit(reset_surface, (text_x, text_y))

        transparent_surface = pygame.Surface((WINDOW_WIDTH - 30, 210), pygame.SRCALPHA)
        pygame.draw.rect(transparent_surface, (0, 0, 0, 25), pygame.Rect(0, 0, WINDOW_WIDTH - 30, 210), border_radius=10)
        surface.blit(transparent_surface, (15, 15))







        # Top Left Box (Online)
        transparent_surface = pygame.Surface((477, 230), pygame.SRCALPHA)
        pygame.draw.rect(transparent_surface, (0, 0, 0, 25), pygame.Rect(0, 0, 477, 230), border_radius=10)
        surface.blit(transparent_surface, (15, 240))
        pygame.draw.rect(surface, (89, 125, 243), pygame.Rect(15, 240, 10, 230), border_top_left_radius=10, border_bottom_left_radius=10)

        # Join Game
        transparent_surface = pygame.Surface((477, 230), pygame.SRCALPHA)
        pygame.draw.rect(transparent_surface, (0, 0, 0, 18), pygame.Rect(0, 0, 209, 85), border_radius=10)
        surface.blit(transparent_surface, (268, 260))

        join_game_text = medium_font.render("Join", True, (255, 255, 255))
        text_rect = join_game_text.get_rect()
        text_x = 268 + (209 - text_rect.width) // 2
        text_y = 260 + (85 - text_rect.height) // 2
        surface.blit(join_game_text, (text_x, text_y))

        # Create Game
        transparent_surface = pygame.Surface((477, 230), pygame.SRCALPHA)
        pygame.draw.rect(transparent_surface, (0, 0, 0, 18), pygame.Rect(0, 0, 209, 85), border_radius=10)
        surface.blit(transparent_surface, (268, 365))

        create_game_text = medium_font.render("Create", True, (255, 255, 255))
        text_rect = create_game_text.get_rect()
        text_x = 268 + (209 - text_rect.width)// 2
        text_y = 365 + (85 - text_rect.height) // 2
        surface.blit(create_game_text, (text_x, text_y))

        reset_surface = large_font.render(f"Online", True, (255, 255, 255))
        surface.blit(reset_surface, (30, 240))

















        # Top Right Box (Computer)
        transparent_surface = pygame.Surface((477, 230), pygame.SRCALPHA)
        pygame.draw.rect(transparent_surface, (0, 0, 0, 25), pygame.Rect(0, 0, 477, 230), border_radius=10)
        surface.blit(transparent_surface, (507, 240))
        pygame.draw.rect(surface, (89, 125, 243), pygame.Rect(507, 240, 10, 230), border_top_left_radius=10, border_bottom_left_radius=10)

        # Join Game (Top Right)
        transparent_surface = pygame.Surface((477, 230), pygame.SRCALPHA)
        pygame.draw.rect(transparent_surface, (0, 0, 0, 18), pygame.Rect(0, 0, 209, 190), border_radius=10)
        surface.blit(transparent_surface, (760, 260))

        join_game_text = medium_font.render("Play", True, (255, 255, 255))
        text_rect = join_game_text.get_rect()
        text_x = 760 + (209 - text_rect.width) // 2
        text_y = 260 + (190 - text_rect.height) // 2
        surface.blit(join_game_text, (text_x, text_y))



        reset_surface = large_font.render(f"Computer", True, (255, 255, 255))
        surface.blit(reset_surface, (522, 240))










        # Bottom Right Box (Analysis)


        transparent_surface = pygame.Surface((477, 230), pygame.SRCALPHA)
        pygame.draw.rect(transparent_surface, (0, 0, 0, 25), pygame.Rect(0, 0, 477, 230), border_radius=10)
        surface.blit(transparent_surface, (507, 485))
        pygame.draw.rect(surface, (89, 125, 243), pygame.Rect(507, 485, 10, 230), border_top_left_radius=10, border_bottom_left_radius=10)


        # Quick Analisys 
        transparent_surface = pygame.Surface((477, 230), pygame.SRCALPHA)
        pygame.draw.rect(transparent_surface, (0, 0, 0, 18), pygame.Rect(0, 0, 209, 190), border_radius=10)
        surface.blit(transparent_surface, (760, 505))



        join_game_text = medium_font.render("Analyze Last Game", True, (255, 255, 255))
        text_rect = join_game_text.get_rect()
        text_x = 760 + (209 - text_rect.width) // 2
        text_y = 505 + (190 - text_rect.height) // 2
        surface.blit(join_game_text, (text_x, text_y))



        reset_surface = large_font.render(f"Analysis", True, (255, 255, 255))
        surface.blit(reset_surface, (522, 485))


















        # Bottom Left Box (Puzzles)
        transparent_surface = pygame.Surface((477, 230), pygame.SRCALPHA)
        pygame.draw.rect(transparent_surface, (0, 0, 0, 25), pygame.Rect(0, 0, 477, 230), border_radius=10)
        surface.blit(transparent_surface, (15, 485))
        pygame.draw.rect(surface, (89, 125, 243), pygame.Rect(15, 485, 10, 230), border_top_left_radius=10, border_bottom_left_radius=10)

        # Rated Puzzles
        transparent_surface = pygame.Surface((477, 230), pygame.SRCALPHA)
        pygame.draw.rect(transparent_surface, (0, 0, 0, 18), pygame.Rect(0, 0, 209, 190), border_radius=10)
        surface.blit(transparent_surface, (268, 505))

        join_game_text = medium_font.render("Puzzles", True, (255, 255, 255))
        text_rect = join_game_text.get_rect()
        text_x = 268 + (209 - text_rect.width) // 2
        text_y = 505 + (190 - text_rect.height) // 2
        surface.blit(join_game_text, (text_x, text_y))



        reset_surface = large_font.render(f"Puzzles", True, (255, 255, 255))
        surface.blit(reset_surface, (30, 485))
