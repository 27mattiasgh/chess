from PIL import Image

WIDTH = 3840
HEIGHT = 2160



top = (180, 43, 180) #180, 43, 53 for pink, 43, 180, 53 for green
bottom = (60, 140, 220)

gradient_image = Image.new("RGB", (WIDTH, HEIGHT))

for x in range(HEIGHT):
    progress = x / HEIGHT
    r = int(top[0] + (bottom[0] - top[0]) * progress)
    g = int(top[1] + (bottom[1] - top[1]) * progress)
    b = int(top[2] + (bottom[2] - top[2]) * progress)
    line_color = (r, g, b)

    for y in range(WIDTH):
        gradient_image.putpixel((x, y), line_color)

gradient_image.save(r"assets\images\background.png")
print('done!')
