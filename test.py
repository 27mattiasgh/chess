import pygame
import pygame.font

# Initialize pygame
pygame.init()

# Set up the window
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Speech Box Example')






margin = 10
rectangle_width = 300 - 2 * margin
rectangle_x = (window_width - rectangle_width) // 2


font_size = 24
font_color = pygame.Color('white')
font = pygame.font.Font(None, font_size)


text = "This is a sample text that we want to fit within the rectangle. It can be long or short."
words = text.split()


lines = []
current_line = words[0]

for word in words[1:]:
    if font.size(current_line + ' ' + word)[0] <= rectangle_width - 2 * margin:
        current_line += ' ' + word
    else:
        lines.append(current_line)
        current_line = word

lines.append(current_line)
line_height = font.size(lines[0])[1]
text_height = len(lines) * line_height

rectangle_height = text_height + 2 * margin + 5
rectangle_y = (window_height - rectangle_height) // 2
rectangle = pygame.Rect(rectangle_x, rectangle_y, rectangle_width, rectangle_height)

text_x = rectangle.centerx - rectangle_width // 2 + margin
text_y = rectangle.centery - text_height // 2 + margin - 10
pygame.draw.rect(window, pygame.Color('pink'), rectangle)


for line in lines:
    rendered_text = font.render(line, True, font_color)
    window.blit(rendered_text, (text_x, text_y))
    text_y += line_height


pygame.display.update()


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Quit the program
pygame.quit()
