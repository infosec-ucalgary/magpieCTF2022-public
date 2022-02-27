###############################################################################
# Generates new flags using several layers
###############################################################################

from PIL import Image
import os
from random import choice, choices
import uuid
import sys

WIDTH = 800
HEIGHT = 400
BLACK = (0,0,0,255)
RED = (255,0,0,255)

def getFile(dirname, folder):
    while True:
        randomFile = choice(os.listdir(os.path.join(dirname, folder)))
        if randomFile.endswith(".png"):
            return os.path.join(dirname, folder, randomFile)

def pickColour():
    colour = choices(range(256), k=3)
    colour.append(255)
    colour = tuple(colour)
    return(colour)

def paintLayer(pixelMap):
    colour1 = pickColour()
    colour2 = pickColour()
    for i in range(WIDTH):
        for j in range(HEIGHT):
            if pixelMap[i,j] == BLACK:
                pixelMap[i,j] = colour1
            elif pixelMap[i,j] == RED:
                pixelMap[i,j] = colour2
            else:
                continue
    return pixelMap

# get the path
if getattr(sys, 'frozen', False):
    dirname = os.path.dirname(sys.executable)
elif __file__:
    dirname = os.path.dirname(os.path.abspath(__file__))

for i in range(2000):
    fingerprint = Image.open("fingerprint.png")
    division = getFile(dirname, "division")
    divisionLayer = Image.open(division)
    overlay = getFile(dirname, "overlay")
    overlayLayer = Image.open(overlay)
    symbol = getFile(dirname, "symbol")
    symbolLayer = Image.open(symbol)

    # paint the division layer a colour
    divisionPixelMap = divisionLayer.load()
    divisionPixelMap = paintLayer(divisionPixelMap)

    # layer division on base
    fingerprint.paste(divisionLayer, (0,0), divisionLayer)

    # add colour on overlay
    overlayPixelMap = overlayLayer.load()
    overlayPixelMap = paintLayer(overlayPixelMap)

    # layer overlay on base
    fingerprint.paste(overlayLayer, (0,0), overlayLayer)

    # add colour to symbol
    symbolPixelMap = symbolLayer.load()
    symbolPixelMap = paintLayer(symbolPixelMap)

    # layer symbol on base
    fingerprint.paste(symbolLayer, (0,0), symbolLayer)


    # save the image
    fileName = uuid.uuid4().hex
    fileName = "/home/jer/Documents/magpieCTF-2022/mom-and-pops-website-frontend/static/img/nft-flags/" + fileName + ".png"
    fingerprint.save(fileName)