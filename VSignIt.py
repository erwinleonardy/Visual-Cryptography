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

"""
Global Variables
"""
# Try different inputs here (jane.png / jane.jpg)
path = "jane.png"

# signature starting point
signX = 1740
signY = 750
signWidth = 200                 # 200 x 200 pixels 
doubSignSize = signWidth * 2
reconDist = signWidth - 85

"""
Functions
"""
# Open an Image
def open_image(filename, bw):
    path = './input/' + filename

    try:
        image = Image.open(path)

        if (bw == 1):
            image = image.convert('1')  # convert image to black and white
        return image

    except IOError:
        return None
        
# Save Image
def save_image(image, filename):
    path = './output/' + filename + '.png'
    print ("{} has been successfully exported!".format(path))
    image.save(path, optimize=True, format="PNG")
 
# Generate 2 shares
def gen_2shares (image):
    # 1 -> 8bit B/W
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
                
    # export image shares
    image1 = open_image ("cheque.jpg", 0)
    image1.paste(outfile1, (signX, signY))       
    save_image (image1, "cheque/share1")   

    image1 = open_image ("cheque.jpg", 0)
    image1.paste(outfile2, (signX, signY))       
    save_image (image1, "cheque/share2")  

    print()

# Reconstruct the image using two of the shares
def merge_2shares ():
    # read both of the shares
    infile1 = Image.open('./output/cheque/share1.png')
    infile2 = Image.open('./output/cheque/share2.png')

    # extract the shares area
    sign1 = infile1.crop((signX, signY, signX+(doubSignSize), signY+(doubSignSize)))
    sign1.thumbnail((doubSignSize, doubSignSize), Image.ANTIALIAS)
    sign1 = sign1.convert('1')
    save_image (sign1, "signature1")  

    sign2 = infile2.crop((signX, signY, signX+(doubSignSize), signY+(doubSignSize)))
    sign2.thumbnail((doubSignSize, doubSignSize), Image.ANTIALIAS)
    sign2 = sign2.convert('1')
    save_image (sign2, "signature2")  
    print()

    # reconstruct the shares
    outfile = Image.new('1', sign1.size)

    for x in range(sign1.size[0]):
        for y in range(sign1.size[1]):
            outfile.putpixel((x,y), min(sign1.getpixel((x, y)), sign2.getpixel((x, y))))

    save_image (outfile, "recon")    

    # clean the reconstructed shares
    clean_2shares (outfile) 

    # replace the area with white color
    result = Image.open('./output/cheque/share1.png')

    for x in range(signX, signX+(doubSignSize)):
        for y in range(signY, signY+(doubSignSize)):
            result.putpixel((x, y), (255,255,255,255))

    # place the clean shares to it
    overlay_pic(result)

# Resize the reconstructed image 
# and clean the noise
def clean_2shares (inputImg):
    outfile = Image.new("1", [int(dimension / 2) for dimension in inputImg.size], 255)
    length, width = inputImg.size

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
    
    # create transparent layer to be pasted on cheque
    image_trans = Image.new("RGBA", (result.size[0], result.size[1]), (255,255,255,0))

    for y in range (0,result.size[0]):
        for x in range (0, result.size[1]):
            if (outfile.getpixel((x,y)) == 0):
                image_trans.putpixel((x,y), (0,0,0,255))

    save_image (image_trans, "clean2")

# overlay the pic
def overlay_pic (dest):
    source = Image.open("./output/clean2.png")
    dest.paste(source, (signX+reconDist, signY+(reconDist*2)), mask=source)       
    save_image (dest, "cheque/final_img")       

"""
Main function
"""
# img = open_image (path, 1)

# if img != None:
#     gen_2shares (img)
#     merge_2shares()

# else:
#     print("{} not found!".format(path))

"""
Flask Part
"""
from flask import Flask, render_template, request
app = Flask(__name__, template_folder='./src')

@app.route('/')
def default_client():
    try:
        return render_template('client.html')
    except Exception as e:
        return str(e)

@app.route('/bank-generate', methods=['GET', 'POST'])
def bank_generate():
    if request.method == 'GET':
        try:
            return render_template('admin-generation.html')
        except Exception as e:
            return str(e)
    
    elif request.method == 'POST':
        print("Hello")

@app.route('/bank-reconstruct')
def bank_reconstruct():
    try:
        return render_template('admin-reconstruct.html')
    except Exception as e:
        return str(e)

@app.route('/client')
def client():
    try:
        return render_template('client.html')
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run()