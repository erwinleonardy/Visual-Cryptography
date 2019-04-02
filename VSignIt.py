"""
VSignIt
A secure Signing Method

Developed by: Erwin Leonardy
"""

from __future__ import print_function
from PIL import Image
import PIL.ImageOps

import re, time, base64
import random, sys, os

import emailer

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

UPLOAD_FOLDER = './input'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

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
def gen_2shares (email, image):
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
    outfile1.save("./input/bank_share.png", optimize=True, format="PNG")
    outfile2.save("./input/client_share.png", optimize=True, format="PNG")

    # emailer.emailer(email, "./input/client_share.png")

    # send back to bank
    with open("./input/bank_share.png", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())

    os.remove("./input/bank_share.png")
    os.remove("./input/client_share.png")

    return encoded_string

    # image1 = open_image ("cheque.jpg", 0)
    # image1.paste(outfile1, (signX, signY))       
    # save_image (image1, "cheque/share1")   

    # image1 = open_image ("cheque.jpg", 0)
    # image1.paste(outfile2, (signX, signY))       
    # save_image (image1, "cheque/share2")      

# Reconstruct the image using two of the shares
def merge_2shares (clientCheque, bankShare):
    # extract the shares area
    clientShare = clientCheque.crop((signX, signY, signX+(doubSignSize), signY+(doubSignSize)))
    clientShare.thumbnail((doubSignSize, doubSignSize), Image.ANTIALIAS)
    clientShare = clientShare.convert('1')

    # reconstruct the shares
    outfile = Image.new('1', clientShare.size)

    for x in range(clientShare.size[0]):
        for y in range(clientShare.size[1]):
            outfile.putpixel((x,y), min(clientShare.getpixel((x, y)), bankShare.getpixel((x, y))))

    save_image (outfile, "recon")    

    # clean the reconstructed shares
    clean_2shares (outfile) 

    # replace the area with white color
    # result = Image.open('./output/cheque/share1.png')

    for x in range(signX, signX+(doubSignSize)):
        for y in range(signY, signY+(doubSignSize)):
            clientCheque.putpixel((x, y), 255)

    # place the clean shares to it
    overlay_pic("./output/clean2.png", clientCheque)

    with open("./output/final_cheque.png", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())

    os.remove("./output/final_cheque.png")

    return encoded_string

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

# paste the source pic on top of the destination pic
def paste_on_top (source, dest):
    dest.paste (source,(signX, signY))   

    # export the image to base64 format
    save_image (dest, "final_img")      

    with open("./output/final_img.png", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())

    os.remove("./output/final_img.png")

    return encoded_string

# overlay the pic
def overlay_pic (sourcePath, dest):
    source = Image.open(sourcePath)
    dest.paste(source, (signX+reconDist, signY+(reconDist*2)), mask=source)       
    save_image (dest, "final_cheque")   

# checks image dimension is a square
# if yes, return the resized image
# otherwise, return None
def validate_resize_image (image):
    width, height = image.size
    if (width != height):
        return None
    else:
        try:
            image.thumbnail((signWidth, signWidth), Image.ANTIALIAS)
            return image
        except IOError:
            return None

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
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
        # print(request.form['file'], file=sys.stderr)

        # convert the base64 image to an image
        base64_data = re.sub('^data:image/.+;base64,', '', request.form['file'])
        byte_data = base64.b64decode(base64_data)

        with open("./input/imageToSave.png", "wb") as fh:
            fh.write(byte_data)

        # generate two shares and send one of the shares to the server
        image = open_image ("imageToSave.png", 1)

        if validate_resize_image(image) != None:
            email = request.form['email']
            bank_share = gen_2shares(email, image)

            os.remove("./input/imageToSave.png")
            return bank_share

        else:
            return ""

@app.route('/bank-reconstruct', methods=['GET', 'POST'])
def bank_reconstruct():
    if request.method == 'GET':
        try:
            return render_template('admin-reconstruct.html')
        except Exception as e:
            return str(e)

    elif request.method == 'POST':        
        # print(request.form['file1'], file=sys.stderr)

        # convert the base64 image to an image
        base64_data1 = re.sub('^data:image/.+;base64,', '', request.form['file1'])
        byte_data1 = base64.b64decode(base64_data1)

        base64_data2 = re.sub('^data:image/.+;base64,', '', request.form['file2'])
        byte_data2 = base64.b64decode(base64_data2)

        with open("./input/clientCheque.png", "wb") as fh:
            fh.write(byte_data1)

        with open("./input/bankShare.png", "wb") as fh:
            fh.write(byte_data2)

        # merge the client cheque and the bank share
        # to reveal the reconstructed signature
        clientCheque = open_image ("clientCheque.png", 1)
        bankShare = open_image ("bankShare.png", 1)

        final_result = merge_2shares (clientCheque, bankShare)

        os.remove("./input/clientCheque.png")
        os.remove("./input/bankShare.png")

        return final_result
        
@app.route('/client', methods=['GET', 'POST'])
def client():
    if request.method == 'GET':
        try:
            return render_template('client.html')
        except Exception as e:
            return str(e)

    elif request.method == 'POST':        
        # print(request.form['file1'], file=sys.stderr)

        # convert the base64 image to an image
        base64_data1 = re.sub('^data:image/.+;base64,', '', request.form['file1'])
        byte_data1 = base64.b64decode(base64_data1)

        base64_data2 = re.sub('^data:image/.+;base64,', '', request.form['file2'])
        byte_data2 = base64.b64decode(base64_data2)

        with open("./input/clientCheque.png", "wb") as fh:
            fh.write(byte_data1)

        with open("./input/clientShare.png", "wb") as fh:
            fh.write(byte_data2)

        # generate two shares and send one of the shares to the server
        clientCheque = open_image ("clientCheque.png", 1)
        clientShare = open_image ("clientShare.png", 1)

        resultStr = paste_on_top (clientShare, clientCheque)

        os.remove("./input/clientCheque.png")
        os.remove("./input/clientShare.png")

        return resultStr


if __name__ == '__main__':
    app.run()