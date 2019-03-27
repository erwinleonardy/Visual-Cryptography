"""
VSignIt
A secure Signing Method

Developed by: Erwin Leonardy

"""

from __future__ import print_function
from PIL import Image
import PIL.ImageOps

import random
import sys

# Try different inputs here
#  path = "john.png"
path = "jane.jpg"

# Open an Image
def open_image(filename):
    path = './input/' + filename
    image = Image.open(path)
    image = image.convert('1') # convert image to black and white
    
    print("(Image Info)")
    print("Image format: {} \t Image size: {} \t\t Image mode: {}".format(image.format, image.size, image.mode))
    print("\nSystem Log:")
    
    return image

# Save Image
def save_image(image, filename):
    path = './output/' + filename + '.png'
    print ("{} has been successfully exported!".format(path))
    image.save(path)

# Get the pixel from the given image
def get_pixel(image, i, j):
# Inside image bounds?
    width, height = image.size
    if i > width or j > height:
        return None

    # Get Pixel
    pixel = image.getpixel((i, j))
    return pixel
 
# Generate 2 shares
def gen_2shares (image):
    outfile1 = Image.new("1", [dimension * 2 for dimension in image.size])
    outfile2 = Image.new("1", [dimension * 2 for dimension in image.size])

    # horizontal axis
    for x in range(0, image.size[0], 2):
        # vertical axis
        for y in range(0, image.size[1], 2):
            # checks if it is black / white
            sourcepixel = image.getpixel((x, y))
            assert sourcepixel in (0, 255)  # prints error if assert fails
            coinflip = random.random()
           
            # if it is black
            if sourcepixel == 0:
                # pick a complimentary pair
                # i.e.
                # X O   O X
                # O X   X O
                if coinflip < 1/6: 
                    outfile1.putpixel((x * 2, y * 2), 0)
                    outfile1.putpixel((x * 2 + 1, y * 2), 0)
                    outfile1.putpixel((x * 2, y * 2 + 1), 255)
                    outfile1.putpixel((x * 2 + 1, y * 2 + 1), 255)

                    outfile2.putpixel((x * 2, y * 2), 255)
                    outfile2.putpixel((x * 2 + 1, y * 2), 255)
                    outfile2.putpixel((x * 2, y * 2 + 1), 0)
                    outfile2.putpixel((x * 2 + 1, y * 2 + 1), 0)
                
                elif coinflip < 2/6: 
                    outfile1.putpixel((x * 2, y * 2), 255)
                    outfile1.putpixel((x * 2 + 1, y * 2), 255)
                    outfile1.putpixel((x * 2, y * 2 + 1), 0)
                    outfile1.putpixel((x * 2 + 1, y * 2 + 1), 0)

                    outfile2.putpixel((x * 2, y * 2), 0)
                    outfile2.putpixel((x * 2 + 1, y * 2), 0)
                    outfile2.putpixel((x * 2, y * 2 + 1), 255)
                    outfile2.putpixel((x * 2 + 1, y * 2 + 1), 255)

                elif coinflip < 3/6:
                    outfile1.putpixel((x * 2, y * 2), 0)
                    outfile1.putpixel((x * 2 + 1, y * 2), 255)
                    outfile1.putpixel((x * 2, y * 2 + 1), 255)
                    outfile1.putpixel((x * 2 + 1, y * 2 + 1), 0)

                    outfile2.putpixel((x * 2, y * 2), 255)
                    outfile2.putpixel((x * 2 + 1, y * 2), 0)
                    outfile2.putpixel((x * 2, y * 2 + 1), 0)
                    outfile2.putpixel((x * 2 + 1, y * 2 + 1), 255)
               
                elif coinflip < 4/6:
                    outfile1.putpixel((x * 2, y * 2), 255)
                    outfile1.putpixel((x * 2 + 1, y * 2), 0)
                    outfile1.putpixel((x * 2, y * 2 + 1), 0)
                    outfile1.putpixel((x * 2 + 1, y * 2 + 1), 255)

                    outfile2.putpixel((x * 2, y * 2), 0)
                    outfile2.putpixel((x * 2 + 1, y * 2), 255)
                    outfile2.putpixel((x * 2, y * 2 + 1), 255)
                    outfile2.putpixel((x * 2 + 1, y * 2 + 1), 0)
                    
                elif coinflip < 5/6:
                    outfile1.putpixel((x * 2, y * 2), 255)
                    outfile1.putpixel((x * 2 + 1, y * 2), 0)
                    outfile1.putpixel((x * 2, y * 2 + 1), 255)
                    outfile1.putpixel((x * 2 + 1, y * 2 + 1), 0)

                    outfile2.putpixel((x * 2, y * 2), 0)
                    outfile2.putpixel((x * 2 + 1, y * 2), 255)
                    outfile2.putpixel((x * 2, y * 2 + 1), 0)
                    outfile2.putpixel((x * 2 + 1, y * 2 + 1), 255)

                else:
                    outfile1.putpixel((x * 2, y * 2), 0)
                    outfile1.putpixel((x * 2 + 1, y * 2), 255)
                    outfile1.putpixel((x * 2, y * 2 + 1), 255)
                    outfile1.putpixel((x * 2 + 1, y * 2 + 1), 0)

                    outfile2.putpixel((x * 2, y * 2), 255)
                    outfile2.putpixel((x * 2 + 1, y * 2), 0)
                    outfile2.putpixel((x * 2, y * 2 + 1), 0)
                    outfile2.putpixel((x * 2 + 1, y * 2 + 1), 255)
            
            # if it is white
            elif sourcepixel == 255:
                # pick the same pairs
                # i.e.
                # X O   X O
                # O X   O X
                if coinflip < 1/6: 
                    outfile1.putpixel((x * 2, y * 2), 0)
                    outfile1.putpixel((x * 2 + 1, y * 2), 0)
                    outfile1.putpixel((x * 2, y * 2 + 1), 255)
                    outfile1.putpixel((x * 2 + 1, y * 2 + 1), 255)

                    outfile2.putpixel((x * 2, y * 2), 0)
                    outfile2.putpixel((x * 2 + 1, y * 2), 0)
                    outfile2.putpixel((x * 2, y * 2 + 1), 255)
                    outfile2.putpixel((x * 2 + 1, y * 2 + 1), 255)
                
                elif coinflip < 2/6: 
                    outfile1.putpixel((x * 2, y * 2), 255)
                    outfile1.putpixel((x * 2 + 1, y * 2), 255)
                    outfile1.putpixel((x * 2, y * 2 + 1), 0)
                    outfile1.putpixel((x * 2 + 1, y * 2 + 1), 0)

                    outfile2.putpixel((x * 2, y * 2), 255)
                    outfile2.putpixel((x * 2 + 1, y * 2), 255)
                    outfile2.putpixel((x * 2, y * 2 + 1), 0)
                    outfile2.putpixel((x * 2 + 1, y * 2 + 1), 0)

                elif coinflip < 3/6:
                    outfile1.putpixel((x * 2, y * 2), 0)
                    outfile1.putpixel((x * 2 + 1, y * 2), 255)
                    outfile1.putpixel((x * 2, y * 2 + 1), 255)
                    outfile1.putpixel((x * 2 + 1, y * 2 + 1), 0)

                    outfile2.putpixel((x * 2, y * 2), 0)
                    outfile2.putpixel((x * 2 + 1, y * 2), 255)
                    outfile2.putpixel((x * 2, y * 2 + 1), 255)
                    outfile2.putpixel((x * 2 + 1, y * 2 + 1), 0)
               
                elif coinflip < 4/6:
                    outfile1.putpixel((x * 2, y * 2), 255)
                    outfile1.putpixel((x * 2 + 1, y * 2), 0)
                    outfile1.putpixel((x * 2, y * 2 + 1), 0)
                    outfile1.putpixel((x * 2 + 1, y * 2 + 1), 255)

                    outfile2.putpixel((x * 2, y * 2), 255)
                    outfile2.putpixel((x * 2 + 1, y * 2), 0)
                    outfile2.putpixel((x * 2, y * 2 + 1), 0)
                    outfile2.putpixel((x * 2 + 1, y * 2 + 1), 255)
                    
                elif coinflip < 5/6:
                    outfile1.putpixel((x * 2, y * 2), 255)
                    outfile1.putpixel((x * 2 + 1, y * 2), 0)
                    outfile1.putpixel((x * 2, y * 2 + 1), 255)
                    outfile1.putpixel((x * 2 + 1, y * 2 + 1), 0)

                    outfile2.putpixel((x * 2, y * 2), 255)
                    outfile2.putpixel((x * 2 + 1, y * 2), 0)
                    outfile2.putpixel((x * 2, y * 2 + 1), 255)
                    outfile2.putpixel((x * 2 + 1, y * 2 + 1), 0)

                else:
                    outfile1.putpixel((x * 2, y * 2), 0)
                    outfile1.putpixel((x * 2 + 1, y * 2), 255)
                    outfile1.putpixel((x * 2, y * 2 + 1), 255)
                    outfile1.putpixel((x * 2 + 1, y * 2 + 1), 0)

                    outfile2.putpixel((x * 2, y * 2), 0)
                    outfile2.putpixel((x * 2 + 1, y * 2), 255)
                    outfile2.putpixel((x * 2, y * 2 + 1), 255)
                    outfile2.putpixel((x * 2 + 1, y * 2 + 1), 0)
                
    save_image (outfile1, "out1")
    save_image (outfile2, "out2")

# Reconstruct the image using two of the shares
def merge_2shares ():
    file1 = ('./output/out1.png')
    file2 = ('./output/out2.png')

    infile1 = Image.open(file1)
    infile2 = Image.open(file2)

    outfile = Image.new('1', infile1.size)

    for x in range(infile1.size[0]):
        for y in range(infile1.size[1]):
            outfile.putpixel((x,y), min(infile1.getpixel((x, y)), infile2.getpixel((x, y))))

    save_image (outfile, "recon")

    # clean the reconstructed shares
    clean_2shares (outfile)

# Resize the reconstructed image 
# and clean the noise
def clean_2shares (inputImg):
    outfile = Image.new("1", [int(dimension / 2) for dimension in inputImg.size], 255)
    length = inputImg.size[0]
    width = inputImg.size[1]

    # Cleaning (Phase 1)
    # only writes black iff
    # the (2x2) block is black
    # i.e.
    # B B
    # B B
    for yIn, yOut in zip(range(0,width,2), range(width)):
        for xIn, xOut in zip(range(0,length,2), range(length)):
            if (inputImg.getpixel((xIn, yIn)) != 255 and
                inputImg.getpixel((xIn + 1, yIn)) != 255 and
                inputImg.getpixel((xIn, yIn + 1)) != 255 and
                inputImg.getpixel((xIn + 1, yIn + 1)) != 255):
                outfile.putpixel((xOut, yOut), 0)

    save_image (outfile, "clean1")
 
    # Cleaning (Phase 2)
    # only writes black iff
    # the block has following pattern
    # i.e.
    # W B  =>  W W
    # B B      W W
    result = outfile
    for y in range (0,result.size[0], 2):
        for x in range (0, result.size[1], 2):
            if (outfile.getpixel((x,y)) == 255 and
                outfile.getpixel((x + 1, y)) == 0 and
                outfile.getpixel((x, y + 1)) == 0 and
                outfile.getpixel((x + 1, y + 1)) == 0):
                result.putpixel((x + 1, y), 255)
                result.putpixel((x, y + 1), 255)
                result.putpixel((x + 1, y + 1), 255)
    
    save_image (outfile, "clean2")

"""
Main function
"""
img = open_image (path)

gen_2shares (img)

outfile = merge_2shares()


