# Filename: shareSplitter.py
# Author: Erwin Leonardy
# Descrption: This file contains all of the necessary functions to split the shares

import PIL.ImageOps, random, base64, os
from sqlalchemy.exc import IntegrityError
from flask_login import current_user
from PIL import Image

from vsignit.models import User, UserType, Client_Data, Bank_Data
from vsignit.emailerService import EmailerService
from vsignit.common import Common
from vsignit import db

class ShareSplitter():
  # Function resizes to the desired dimension (200 x 200)
  @staticmethod
  def resize(image):
    return image.resize((200, 200))

  # Function split image into two shares using (2,2) Basic VC Scheme
  @staticmethod
  def create_shares(image):
    pattern = ((0,0,255,255), (255,255,0,0), (0,255,255,0), (255,0,0,255), (255,0,255,0), (0,255,0,255))

      # 1 -> 8bit B/W
    share1 = Image.new("1", [dimension * 2 for dimension in image.size])
    share2 = Image.new("1", [dimension * 2 for dimension in image.size])
    
    # horizontal axis
    for x in range(0, image.size[0], 2):
      # vertical axis
      for y in range(0, image.size[1], 2):
        # checks if it is black / white
        sourcepixel = image.getpixel((x, y))
        assert sourcepixel in (0, 255)  # prints error if assert fails
        pat = random.choice(pattern)

        # always get one share
        share1.putpixel((x * 2, y * 2), pat[0])
        share1.putpixel((x * 2 + 1, y * 2), pat[1])
        share1.putpixel((x * 2, y * 2 + 1), pat[2])
        share1.putpixel((x * 2 + 1, y * 2 + 1), pat[3])
    
        # if it is black
        # pick a complimentary pair
        # i.e.
        # X O   O X
        # O X   X O
        if sourcepixel == 0:
          share2.putpixel((x * 2, y * 2), 255 - pat[0])
          share2.putpixel((x * 2 + 1, y * 2), 255 - pat[1])
          share2.putpixel((x * 2, y * 2 + 1), 255 - pat[2])
          share2.putpixel((x * 2 + 1, y * 2 + 1), 255 - pat[3])
        
        # if it is white
        # pick the same pairs
        # i.e.
        # X O   X O
        # O X   O X
        elif sourcepixel == 255:
          share2.putpixel((x * 2, y * 2), pat[0])
          share2.putpixel((x * 2 + 1, y * 2), pat[1])
          share2.putpixel((x * 2, y * 2 + 1), pat[2])
          share2.putpixel((x * 2 + 1, y * 2 + 1), pat[3])
      
    return share1, share2

  # Function sends client/bank shares to respective emails
  @staticmethod
  def store_shares(share1, share2, username):
    bank_userid = current_user.get_id()
    client_userid = User.query.filter_by(username=username).first().id
    bank_username = User.query.filter_by(id=bank_userid).first().username

    # export image shares
    bank_share_path = "./vsignit/output/bank/" + username + "_" + bank_username + "_bank_share.png"
    client_share_path = "./vsignit/output/client/" + username + "_" + bank_username + "_client_share.png"
    Common.save_image(share1, bank_share_path)
    Common.save_image(share2, client_share_path)

    # checks if data already exists
    existingBank = Bank_Data.query.get([bank_userid, client_userid])
    existingClient = Client_Data.query.get([client_userid, bank_userid])

    # if yes, overwrites it
    if existingBank != None and existingClient != None:
      existingBank.bank_share_path = bank_share_path
      existingClient.client_share_path = client_share_path 
      db.session.commit()     
      return "You have just overwritten \'" + username + "\' client and bank shares!"

    # else, creates a new record
    else:     
      newBankData = Bank_Data(bank_userid, client_userid, bank_share_path)
      newClientData = Client_Data(client_userid, bank_userid, client_share_path)
      db.session.add(newBankData)
      db.session.add(newClientData)
      db.session.commit()
      return "Bank share and user shares have been created and stored!"

    # email share to the client
    # emailer = EmailerService()
    # emailer.sendShare(email, client_sharename)

    # convert the image into base64
    # with open(bank_share_path, "rb") as image_file:
    #     encoded_string = base64.b64encode(image_file.read())

    # delete the temp files
    # os.remove(bank_sharename)
    # os.remove(client_sharename)

    # send back bank share to the bank using AJAX

    # image1 = open_image ("cheque.jpg", 0)
    # image1.paste(outfile1, (signX, signY))       
    # save_image (image1, "cheque/share1")  