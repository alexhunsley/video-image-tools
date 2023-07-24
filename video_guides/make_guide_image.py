# make_guide_image.py

import sys
from PIL import Image, ImageDraw, ImageFont

# Set up parameters
width, height = 1920, 1080
grid_size = 16
line_color = (0, 255, 0, 255)  # green in RGBA format
text_color = (255, 255, 255, 255)  # white in RGBA format
shadow_color = (0, 0, 0, 255)  # black in RGBA format
# shadow_color = (255, 0, 0, 255)  # black in RGBA format

# Create a new image with transparency
image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
# image = Image.new('RGBA', (width, height), (255, 255, 255, 255))

# Create a draw object
draw = ImageDraw.Draw(image)

# from https://www.fontspace.com/sparkly-font-f11575
font = ImageFont.truetype("SparklyFontRegular-zyA3.ttf", 48)

vertical_text_pos_fudge = -10

# Function to draw text with shadow
def draw_shadow_text(draw, pos, text, font, text_color, shadow_color):
    x, y = pos

    # Pillow 10 way
    (left, top, right, bottom) = draw.textbbox((x, y), text, font=font, anchor='mm') #, align='center')
    text_width = right - left
    text_height = top - bottom

    # print(f"text box size: {tw} {th}")
    # sys.exit(0)

    # text_width, text_height = draw.textsize(text, font)
    # print(f"text box size: {text_width} {text_height}")

    x -= text_width // 2
    y -= text_height // 2 - vertical_text_pos_fudge

    # Draw shadow text
    draw.text((x-1, y), text, fill=shadow_color, font=font)
    draw.text((x+1, y), text, fill=shadow_color, font=font)
    draw.text((x, y-1), text, fill=shadow_color, font=font)
    draw.text((x, y+1), text, fill=shadow_color, font=font)
    # Draw the actual text
    draw.text((x, y), text, fill=text_color, font=font)


grid_offs_x = [x * width / 16.0 for x in range(0,17)]
grid_offs_y = [y * height / 16.0 for y in range(0,17)]

# print(grid_offs_x)
# print(grid_offs_y)
# sys.exit(0)

# vertical shadow lines
for xOffs in range(-1, 2, 2):
    for i in grid_offs_x:
        draw.line([(i + xOffs, 0), (i + xOffs, height)], fill=shadow_color)

# horizontal shadow lines
for yOffs in range(-1, 2, 2):
    for j in grid_offs_y:
        draw.line([(0, j + yOffs), (width, j + yOffs)], fill=shadow_color)


# vertical lines
for i in grid_offs_x:
    draw.line([(i, 0), (i, height)], fill=line_color)

# horizontal lines
for j in grid_offs_y:
    draw.line([(0, j), (width, j)], fill=line_color)


# Draw text within each grid cell
for i in range(grid_size):
    for j in range(grid_size):

        x = f"{i:01x}".upper()
        y = f"{j:01x}".upper()
        
        print(f" made x y : {x} {y}")
        text = f'{x}{y}'  # convert to two-digit hex, then concatenate
    
        text_pos = grid_offs_x[i] + grid_offs_x[1] // 2, grid_offs_y[j] + grid_offs_y[1] // 2

        # text_pos = (x, y)

        # text = f'{i:01x}{j:01x}'  # convert to two-digit hex, then concatenate
        draw_shadow_text(draw, text_pos, text, font, text_color, shadow_color)

# Save the image
image.save('grid.png')



# original pillow:

# ❯ pipdeptree | grep illow
# ├── Pillow [required: Any, installed: 9.2.0]
# │   └── Pillow [required: >=8.0.0, installed: 9.2.0]
# │   └── Pillow [required: >=8.3.2, installed: 9.2.0]

