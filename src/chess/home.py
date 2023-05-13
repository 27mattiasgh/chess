import pygame
from src.chess.const import *
pygame.init()

class Home:
    def __init__(self):
        self.time_period = 25000

    def create_gradient(self, surface, colors):
        width, height = surface.get_size()
        num_steps = width

        time_elapsed = pygame.time.get_ticks() % self.time_period

        num_colors = len(colors)
        color_range = self.time_period // num_colors

        for i in range(num_steps):
            step_time = time_elapsed % color_range
            color_index = time_elapsed // color_range

            start_color = colors[color_index]
            end_color = colors[(color_index + 1) % num_colors]

            progress = (step_time / color_range) ** 2  # Adjusted progress calculation

            r = int(start_color[0] + (end_color[0] - start_color[0]) * progress)
            g = int(start_color[1] + (end_color[1] - start_color[1]) * progress)
            b = int(start_color[2] + (end_color[2] - start_color[2]) * progress)

            rect_color = (r, g, b)
            print(rect_color)
            pygame.draw.rect(surface, rect_color, pygame.Rect(i, 0, 1, height))



    def home(self, surface):
        colors = [(0x3C, 0x8C, 0xDE),(0xED, 0x73, 0xA8)]

        self.create_gradient(surface, colors)

        pygame.draw.rect(surface, (255, 255, 255, 0), pygame.Rect(15, 15, WINDOW_WIDTH - 30, 210), border_radius=10)

        tint_factor = 0.45


        bg_color = surface.get_at((0, 0))
        tinted_color_main = (min(int(bg_color[0] * (1 + (tint_factor + 0.15))), 255), min(int(bg_color[1] * (1 + tint_factor)), 255), min(int(bg_color[2] * (1 + tint_factor)), 255),bg_color[3])
        tinted_color_other = (min(int(bg_color[0] * (1 + tint_factor)), 255), min(int(bg_color[1] * (1 + tint_factor)), 255), min(int(bg_color[2] * (1 + tint_factor)), 255),bg_color[3])


        pygame.draw.rect(surface, tinted_color_main, pygame.Rect(15, 15, WINDOW_WIDTH - 30, 210), border_radius=10)


        pygame.draw.rect(surface, tinted_color_other, pygame.Rect(15, 240, 477, 230), border_radius=10)
        pygame.draw.rect(surface, tinted_color_other, pygame.Rect(507, 240, 477, 230), border_radius=10)
        pygame.draw.rect(surface, tinted_color_other, pygame.Rect(15, 485, 477, 230), border_radius=10)
        pygame.draw.rect(surface, tinted_color_other, pygame.Rect(507, 485, 477, 230), border_radius=10)


    def settings(self, surface):
        pass
