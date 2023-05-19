import pygame
import socket
import netaddr

# Initialize pygame
pygame.init()

# Create a screen with a background
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
background = pygame.Surface(screen.get_size())
background.fill((0, 0, 0))  # Fill with black color


font_size = 40
large_font = pygame.font.Font(None, font_size)


password = ""
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_RETURN:
                if len(password) == 10:
                    running = False

            elif event.key == pygame.K_BACKSPACE:
                password = password[:-1]

                if len(password) < 10:
                    password += str(event.key - pygame.K_KP0)

            elif event.key in [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]:
                if len(password) < 10:
                    password += str(event.key - pygame.K_0)


    screen.blit(background, (0, 0))
    password_text = password.replace("", " ")[1:-1]
    password_rendered = large_font.render(password_text, True, (255, 255, 255))
    password_rect = password_rendered.get_rect()
    password_rect.center = screen.get_rect().center
    screen.blit(password_rendered, password_rect)

   
    pygame.display.update()

# Release resources
pygame.quit()
