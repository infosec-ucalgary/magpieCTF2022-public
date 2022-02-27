###############################################################################
# Reads out and prints the rgb value of each pixel
###############################################################################
from PIL import Image

# Import an image from directory:
input_image = Image.open("recreate.png")
  
# Extracting pixel map:
pixel_map = input_image.load()

# Extracting the width and height 
# of the image:
width, height = input_image.size
  
# taking half of the width:
for i in range(width):
    for j in range(height):
        print(pixel_map[i,j])