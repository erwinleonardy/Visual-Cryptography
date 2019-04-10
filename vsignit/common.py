"""
    common.py
    by: Erwin Leonardy

    This file contains all of the supporting
    functions that are shared across the 
    other python files
"""

from PIL import Image
import PIL.ImageOps
import base64, os

signX = 1740
signY = 750
signWidth = 200                 # 200 x 200 pixels
doubSignSize = signWidth * 2
reconDist = signWidth - 85

class Common():
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

    # paste the source pic on top of the destination pic
    @staticmethod
    def paste_on_top (source, dest, username):
        dest.paste (source,(signX, signY))   

        # export the image to base64 format
        Common.save_image (dest, "final_img")      

        with open("./vsignit/output/final_img.png", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())

        os.remove("./vsignit/output/final_img.png")

        return (encoded_string.decode("utf-8") + "," + username)

    # overlay the pic
    # this preserves the transparency
    @staticmethod
    def overlay_pic (sourcePath, dest):
        source = Image.open(sourcePath)
        dest.paste(source, (signX+reconDist, signY+(reconDist*2)), mask=source)       
        Common.save_image (dest, "final_cheque")   