"""
    shareSplitter.py
    by: Erwin Leonardy

    This file contains all of the necessary
    functions to split the shares
"""

from PIL import Image
import PIL.ImageOps
import random, base64, os

from vsignit.emailerService import EmailerService

class ShareSplitter():
    """
        This function resizes to the desired 
        dimension, which is (200 x 200)
    """
    @staticmethod
    def resize (image):
        return image.resize((200, 200)) 

    """
        This function takes in an image
        and split it into two shares using
        (2,2) Basic VC Scheme
    """
    @staticmethod
    def split_signature (image):
        pattern = ((0,0,255,255), (255,255,0,0), (0,255,255,0), (255,0,0,255), (255,0,255,0), (0,255,0,255))

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
            
        return outfile1, outfile2

    """
        This function sends the client share
        to the client's email provided and 
        the bank's share will be available
        for download
    """
    @staticmethod
    def send_shares (outfile1, outfile2, email, username):
        # export image shares
        bank_sharename = "./vsignit/input/" + username + "_bank_share.png"
        client_sharename = "./vsignit/input/" + username + "_client_share.png"
        outfile1.save(bank_sharename, optimize=True, format="PNG")
        outfile2.save(client_sharename, optimize=True, format="PNG")

        # email share to the client
        emailer = EmailerService()
        emailer.sendShare(email, client_sharename)

        # convert the image into base64
        with open(bank_sharename, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())

        # delete the temp files
        os.remove(bank_sharename)
        os.remove(client_sharename)

        # send back bank share to the bank using AJAX
        return (encoded_string.decode("utf-8")  + ',' + username)

        # image1 = open_image ("cheque.jpg", 0)
        # image1.paste(outfile1, (signX, signY))       
        # save_image (image1, "cheque/share1")  