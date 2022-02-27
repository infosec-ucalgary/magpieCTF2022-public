###############################################################################
# Test script for image alteration.  This makes an image greyscale
###############################################################################

from PIL import Image
import random

def greyscale(r, g, b):
    grayscale = (0.299*r + 0.587*g + 0.114*b)
    return int(grayscale)
  
# Import an image from directory:
input_image = Image.open("base-test.png")
  
# Extracting pixel map:
pixel_map = input_image.load()
  
# Extracting the width and height 
# of the image:
width, height = input_image.size
  
# taking half of the width:
for i in range(width):
    for j in range(height):

        print(i)
        print(j)
        
        # getting the RGB pixel value.
        r, g, b, a = input_image.getpixel((i, j))

        # decide how to manipulate
        random_number = 11 #random.randint(1,10)

        if random_number < 4:
            pixel_map[i,j] = (greyscale(r,g,b), greyscale(r,g,b), greyscale(r,g,b))

        elif random_number > 4 and random_number < 7:
            pixel_map[i,j] = (random.randint(1,256), random.randint(1,256), random.randint(1,256))
        
        else:
            r = random.randint(251, 255)
            g = random.randint(251, 255)
            b = random.randint(251, 255)
            pixel_map[i,j] = (r,g,b)

# Saving the final output
# as "grayscale.png":
input_image.save("repro.png")
  
# use input_image.show() to see the image on the
# output screen.