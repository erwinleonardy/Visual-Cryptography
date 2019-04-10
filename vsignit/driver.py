"""
    routes.py
    by: Erwin Leonardy

    This file contains all of the necessary
    functions to run the web application.
"""

from __future__ import print_function
from PIL import Image
import PIL.ImageOps
import re, time, base64, sys, os

from vsignit.shareSplitter import ShareSplitter

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

    """
        Share Splitter Driver Function
    """
    @staticmethod
    def share_splitter (email, image, username):
        # resize the image
        image = ShareSplitter.resize(image)

        # split into two shares
        outfile1, outfile2 = ShareSplitter.split_signature (image)

        # send the shares to the 
        encoded_str = ShareSplitter.send_shares (outfile1, outfile2, email, username)

        return encoded_str

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