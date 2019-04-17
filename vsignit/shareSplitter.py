"""
    shareSplitter.py
    by: Erwin Leonardy

    This file contains all of the necessary
    functions to split the shares
"""

from PIL import Image
import PIL.ImageOps
import random, base64, os
from flask_login import current_user
from sqlalchemy.exc import IntegrityError

from vsignit import db
from vsignit.models import User, UserType, Client_Data, Bank_Data
from vsignit.emailerService import EmailerService
from vsignit.common import Common

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
    def send_shares (outfile1, outfile2, username):
        bank_userid = current_user.get_id()
        client_userid = User.query.filter_by(username=username).first().id
        bank_username = User.query.filter_by(id=bank_userid).first().username

        # export image shares
        bank_share_path = "./vsignit/output/bank/" + username + "_" + bank_username + "_bank_share.png"
        client_share_path = "./vsignit/output/client/" + username + "_" + bank_username + "_client_share.png"
        Common.save_image(outfile1, bank_share_path)
        Common.save_image(outfile2, client_share_path)

        # checks if data already exists
        existingBank = Bank_Data.query.get([bank_userid, client_userid])
        existingClient = Client_Data.query.get([client_userid, bank_userid])

        # if yes, overwrites it
        if existingBank != None and existingClient != None:
            existingBank.bank_share_path = bank_share_path
            existingClient.client_share_path = client_share_path      

        # else, creates a new record
        else:     
            newBankData = Bank_Data(bank_userid, client_userid, bank_share_path)
            newClientData = Client_Data(client_userid, bank_userid, client_share_path)
            db.session.add(newBankData)
            db.session.add(newClientData)
        
        db.session.commit()

        # email share to the client
        # emailer = EmailerService()
        # emailer.sendShare(email, client_sharename)

        # convert the image into base64
        with open(bank_share_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())

        # delete the temp files
        # os.remove(bank_sharename)
        # os.remove(client_sharename)

        # send back bank share to the bank using AJAX
        return (encoded_string.decode("utf-8"))

        # image1 = open_image ("cheque.jpg", 0)
        # image1.paste(outfile1, (signX, signY))       
        # save_image (image1, "cheque/share1")  