from PIL import Image
import random

lower_limit = 251
upper_limit = 255

# Create a new image
new_image = Image.new('RGBA', (800, 400), (0,0,0,0))

new_map = new_image.load()
  
# Extracting the width and height 
# of the image:
width, height = new_image.size
  
# taking half of the width:
for i in range(width):
    for j in range(height):

        r = random.randint(lower_limit, upper_limit)
        g = random.randint(lower_limit, upper_limit)
        b = random.randint(lower_limit, upper_limit)
        a = random.randint(lower_limit, upper_limit)
        new_map[i,j] = (r,g,b,a)

new_image.save("base-pattern.png")