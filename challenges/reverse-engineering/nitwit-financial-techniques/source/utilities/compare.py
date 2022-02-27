###############################################################################
# Compares two images and tels you which pixels do not match.  Also creates
# a new image where each coloured pixel is a pixel that doesn't match in the
# two images
###############################################################################
from PIL import Image

# Import an image from directory:
base_image = Image.open("base-pattern.png")
  
# Extracting pixel map:
base_pixel_map = base_image.load()

# Import an image from directory:
recreate_image = Image.open("recreate.png")
  
# Extracting pixel map:
recreate_map = recreate_image.load()

# Create a new image
new_image = Image.new('RGBA', (800, 400), (0,0,0,0))
new_map = new_image.load()

# get image size
width, height = base_image.size

# mismatched pixel count
mismatch = 0
match = 0

for i in range(width):
    for j in range(height):
        if base_pixel_map[i,j] != recreate_map[i,j]:
            new_map[i,j] = (255,0,0,255)
            mismatch += 1
        else:
            match += 1

print("Mismatched pixels: " + str(mismatch))
print("Matched pixels: " + str(match))
new_image.save("bad_pixels2.png")