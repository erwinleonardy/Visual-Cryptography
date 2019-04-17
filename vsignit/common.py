"""
    common.py
    by: Erwin Leonardy

    This file contains all of the supporting
    functions that are shared across the 
    other python files
"""

from PIL import Image
import PIL.ImageOps
import base64, os, time, datetime

from vsignit.models import User, Client_Data

signX = 1740
signY = 750
signWidth = 200                 # 200 x 200 pixels
doubSignSize = signWidth * 2
reconDist = signWidth - 85

class Common():
    # Open an Image
    @staticmethod
    def open_image(path, bw):
        try:
            image = Image.open(path)

            if bw == 1:
                image = image.convert('1')  # convert image to black and white
            return image

        except IOError:
            return None

    # Save Image
    @staticmethod
    def save_image(image, filepath):
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        print("({}) {} has been successfully exported!".format(st, filepath))
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        image.save(filepath, optimize=True, format="PNG")

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

        # save the file temporarily
        filepath = "./vsignit/output/tmp/" + username + "_final_cheque.png"
        Common.save_image (dest, filepath)      

        # export the image to base64 format
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())

        os.remove(filepath)

        return (encoded_string.decode("utf-8") + "," + username)

    # overlay the pic
    # this preserves the transparency
    @staticmethod
    def overlay_pic (sourcePath, dest):
        source = Image.open(sourcePath)
        dest.paste(source, (signX+reconDist, signY+(reconDist*2)), mask=source)       
        Common.save_image (dest, "final_cheque")   

    # this function checks if the client's
    # username given by the bank exists
    @staticmethod
    def userExists(username):
        if User.query.filter_by(username=username).first() == None:
            return None
        else:
            return "OK"

    @staticmethod
    def getBankUsernames (userid):
        # get the banks this particular client subscribed
        bank_subcribed = Client_Data.query.filter_by(client_userid=userid).all()

        print(bank_subcribed)
        print("\n\n\n\n")

        usernames = []

        for bank in bank_subcribed:
            usernames.append(Common.getBankUsernameFromID(bank.getBankUserId()))

        return usernames

    @staticmethod
    def getBankUsernameFromID (userid):
        username = User.query.filter_by(id=userid).first().getUsername() 
        return username