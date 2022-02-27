###############################################################################
# Script for each Mom & Pops NFT flags and recreating the "fingerprint" base
# layer that is common to all the images
###############################################################################

from PIL import Image
import os

# set image height and width
WIDTH = 800
HEIGHT = 400

# set number of pixels
pixels = WIDTH * HEIGHT

# get directory with the flag images
flags = len(os.listdir("genflags"))

# function to figure out the most common pixel for that position
def most_frequent(List):
    return max(set(List), key = List.count)

# 3d array to hold each pixel (WIDTH x HEIGHT) for each image
arr = [[[0 for k in range(flags)] for j in range(WIDTH)] for i in range(HEIGHT)]

# counter for the file being loaded
file = 0

# loop to load the pixel of each image into the array 
for filename in os.listdir("genflags"):
    # open the image
    sampleImage = Image.open("genflags/" + filename)
    # create a pixel map from the loaded image
    pixelMap = sampleImage.load()
    # for each pixel
    for i in range(WIDTH):
        for j in range(HEIGHT):
            # add the pixel values into the 3d array
            arr[j][i][file] = pixelMap[i,j]
    file += 1
    print("Analyzing file: " + str(file))

print("")
print("BUILDING NEW IMAGE!")
print("")

# create new image
new_image = Image.new('RGBA', (WIDTH, HEIGHT), (0,0,0,0))

# load the pixel map of the new image
new_map = new_image.load()

# counter for the pixel being analyzed
pixel = 0

# for each pixel in the 3d array
for i in range(WIDTH):
    for j in range(HEIGHT):

        # get the most frequent pixel value in the map at those coordinates
        # assign that value to the new fingerprint image
        new_map[i,j] = most_frequent(arr[j][i])

        # print which pixel was just analyzed for tacking purposes
        print("Done pixel: " + str(pixel))
        pixel += 1

# save the rebuild "fingerprint"
new_image.save("recreate.png")