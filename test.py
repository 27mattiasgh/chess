import pygame
import time

WIDTH = 800
HEIGHT = 800
LINE_SPACING = 1
LINE_COUNT = int(HEIGHT / LINE_SPACING)
FRAME_DELAY = 0.01  # Delay in seconds between frame updates

def create_gradient():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Moving Gradient Background")

    gradient_surface = pygame.Surface((WIDTH, HEIGHT))

    running = True
    start_color = (0, 0, 0)  # Blue color
    end_color = (255, 255, 255)   # Pink color

    # Pre-generate the lines of the gradient
    lines = []
    for y in range(HEIGHT):
        progress = y / HEIGHT
        if progress < 0.5:
            # Blue to Pink transition
            r = int(start_color[0] + (end_color[0] - start_color[0]) * (progress * 2))
            g = int(start_color[1] + (end_color[1] - start_color[1]) * (progress * 2))
            b = int(start_color[2] + (end_color[2] - start_color[2]) * (progress * 2))
        else:
            # Pink to Blue transition
            r = int(end_color[0] + (start_color[0] - end_color[0]) * ((progress - 0.5) * 2))
            g = int(end_color[1] + (start_color[1] - end_color[1]) * ((progress - 0.5) * 2))
            b = int(end_color[2] + (start_color[2] - end_color[2]) * ((progress - 0.5) * 2))
        lines.append(((0, y), (WIDTH, y), (r, g, b)))

    offset = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update the offset to create the moving effect
        offset = (offset + 1) % LINE_COUNT

        # Clear the gradient surface
        gradient_surface.fill((0, 0, 0))

        # Draw the lines with updated positions
        for i in range(LINE_COUNT):
            line = lines[i]
            line_y = (line[0][1] + offset) % HEIGHT
            pygame.draw.line(gradient_surface, line[2], (0, line_y), (WIDTH, line_y))

        screen.blit(gradient_surface, (0, 0))
        pygame.display.update()

        # Introduce a delay to control the speed
        time.sleep(FRAME_DELAY)

    pygame.quit()

create_gradient()
