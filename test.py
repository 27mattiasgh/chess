import pygame

# Define the box dimensions
box_width = 200
box_height = 100

# Define the text content
text_content = "This is a long text that needs to fit within the box"

# Initialize Pygame
pygame.init()

# Create a font object
font = pygame.font.Font(None, 30)  # Start with an initial font size

# Iterate and decrease the font size until the text fits within the box
while font.size(text_content)[0] > box_width or font.size(text_content)[1] > box_height:
    font_size = font.get_size()
    font = pygame.font.Font(None, font_size - 1)

# Render the text
text_surface = font.render(text_content, True, (255, 255, 255))

# Create a surface for the box
box_surface = pygame.Surface((box_width, box_height))
box_surface.fill((0, 0, 0))  # Fill the box with a black color

# Calculate the center position for the text
text_x = (box_width - text_surface.get_width()) // 2
text_y = (box_height - text_surface.get_height()) // 2

# Blit the text onto the box surface
box_surface.blit(text_surface, (text_x, text_y))

# Initialize the screen
screen = pygame.display.set_mode((box_width, box_height))
pygame.display.set_caption("Text Fit Example")

# Blit the box surface onto the screen
screen.blit(box_surface, (0, 0))
pygame.display.flip()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
