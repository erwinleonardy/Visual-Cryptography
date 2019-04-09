"""
    routes.py
    by: Erwin Leonardy

    This file contains all of the necessary
    functions to run the web application.
"""

from __future__ import print_function
from PIL import Image
import PIL.ImageOps
import re, time, base64, random, sys, os

from vsignit.emailerService import EmailerService

"""
Global Variables
"""
# signature starting point
signX = 1740
signY = 750
signWidth = 200                 # 200 x 200 pixels
doubSignSize = signWidth * 2
reconDist = signWidth - 85

"""
Functions
"""
class Driver():
    # Open an Image
    @staticmethod
    def open_image(filename, bw):
        path = './vsignit/input/' + filename

        try:
            image = Image.open(path)

            if bw == 1:
                image = image.convert('1')  # convert image to black and white
            return image

        except IOError:
            return None

    # Save Image
    @staticmethod
    def save_image(image, filename):
        path = './vsignit/output/' + filename + '.png'
        print("{} has been successfully exported!".format(path))
        image.save(path, optimize=True, format="PNG")

    # Generate 2 shares
    @staticmethod
    def gen_2shares (email, image, username):
        pattern = ((0,0,255,255), (255,255,0,0), (0,255,255,0), (255,0,0,255), (255,0,255,0), (0,255,0,255))

        # resize image
        image = image.resize((200, 200))

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
                pat = random.choice(pattern)

                # always get one share
                outfile1.putpixel((x * 2, y * 2), pat[0])
                outfile1.putpixel((x * 2 + 1, y * 2), pat[1])
                outfile1.putpixel((x * 2, y * 2 + 1), pat[2])
                outfile1.putpixel((x * 2 + 1, y * 2 + 1), pat[3])
            
                # if it is black
                # pick a complimentary pair
                # i.e.
                # X O   O X
                # O X   X O
                if sourcepixel == 0:
                    outfile2.putpixel((x * 2, y * 2), 255 - pat[0])
                    outfile2.putpixel((x * 2 + 1, y * 2), 255 - pat[1])
                    outfile2.putpixel((x * 2, y * 2 + 1), 255 - pat[2])
                    outfile2.putpixel((x * 2 + 1, y * 2 + 1), 255 - pat[3])
                
                # if it is white
                # pick the same pairs
                # i.e.
                # X O   X O
                # O X   O X
                elif sourcepixel == 255:
                    outfile2.putpixel((x * 2, y * 2), pat[0])
                    outfile2.putpixel((x * 2 + 1, y * 2), pat[1])
                    outfile2.putpixel((x * 2, y * 2 + 1), pat[2])
                    outfile2.putpixel((x * 2 + 1, y * 2 + 1), pat[3])

        # export image shares
        bank_sharename = "./vsignit/input/" + username + "_bank_share.png"
        client_sharename = "./vsignit/input/" + username + "_client_share.png"
        outfile1.save(bank_sharename, optimize=True, format="PNG")
        outfile2.save(client_sharename, optimize=True, format="PNG")

        # email share to the client
        emailer = EmailerService()
        emailer.sendShare(email, client_sharename)

        # send back bank share to the bank using AJAX
        with open(bank_sharename, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())

        os.remove(bank_sharename)
        os.remove(client_sharename)

        return (encoded_string.decode("utf-8")  + ',' + username)

        # image1 = open_image ("cheque.jpg", 0)
        # image1.paste(outfile1, (signX, signY))       
        # save_image (image1, "cheque/share1")   

    # Reconstruct the image using two of the shares
    @staticmethod
    def merge_2shares (clientCheque, bankShare, username):
        bankWidth, bankHeight = bankShare.size
        signWidth = int(bankWidth / 2)
        doubSignSize = signWidth * 2

        # extract the shares area
        clientShare = clientCheque.crop((signX, signY, signX+(doubSignSize), signY+(doubSignSize)))
        clientShare.thumbnail((doubSignSize, doubSignSize), Image.ANTIALIAS)
        clientShare = clientShare.convert('1')
        clientWidth, clientHeight = clientShare.size

        print("clientWidth: {}, clientHeight: {}".format(clientWidth, clientHeight))
        print("bankWidth: {}, bankHeight: {}".format(bankWidth, bankHeight))

        if (bankWidth == clientWidth and bankHeight == clientHeight): 
            try:
                # reconstruct the shares
                outfile = Image.new('1', clientShare.size)

                for x in range(clientShare.size[0]):
                    for y in range(clientShare.size[1]): 
                        outfile.putpixel((x,y), min(clientShare.getpixel((x, y)), bankShare.getpixel((x, y))))

                Driver.save_image (outfile, "recon")    

                # clean the reconstructed shares
                Driver.clean_2shares (outfile) 

                # replace the area with white color
                for x in range(signX, signX+(doubSignSize)):
                    for y in range(signY, signY+(doubSignSize)):
                        clientCheque.putpixel((x, y), 255)

                # place the clean shares to it
                Driver.overlay_pic("./vsignit/output/clean2.png", clientCheque)

                # send back the final cheque to the bank using AJAX
                with open("./vsignit/output/final_cheque.png", "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read())

                os.remove("./vsignit/output/final_cheque.png")

                return (encoded_string.decode("utf-8") + "," + username)
            
            except IndexError:
                return ""

        else:
            return ""

    # Resize the reconstructed image and clean the noise
    @staticmethod
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

        Driver.save_image (outfile, "clean1")
    
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

        Driver.save_image (image_trans, "clean2")

    # paste the source pic on top of the destination pic
    @staticmethod
    def paste_on_top (source, dest, username):
        dest.paste (source,(signX, signY))   

        # export the image to base64 format
        Driver.save_image (dest, "final_img")      

        with open("./vsignit/output/final_img.png", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())

        os.remove("./vsignit/output/final_img.png")

        return (encoded_string.decode("utf-8") + "," + username)

    # overlay the pic
    @staticmethod
    def overlay_pic (sourcePath, dest):
        source = Image.open(sourcePath)
        dest.paste(source, (signX+reconDist, signY+(reconDist*2)), mask=source)       
        Driver.save_image (dest, "final_cheque")   

    # checks image dimension is a square
    # if yes, return the resized image
    # otherwise, return None
    @staticmethod
    def validate_resize_image (image):
        width, height = image.size
        if (width != height):
            return None
    
        else:
            try:
                image.resize((signWidth, signWidth))
                img_w, img_h = image.size
                background = Image.new('1', (signWidth, signWidth), 255)
                bg_w, bg_h = background.size
                offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)
                background.paste(image, offset)
                return image

            except IOError:
                return None