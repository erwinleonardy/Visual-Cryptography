# Filename: common.py
# Author: Erwin Leonardy
# Descrption: This file contains all of the supporting functions that are shared across the 
#             other python files

import PIL.ImageOps, os, time, datetime
from sqlalchemy import desc
from PIL import Image

from vsignit.models import User, Client_Data, Transaction

signX = 1740
signY = 750
signWidth = 200                 # 200 x 200 pixels
doubSignSize = signWidth * 2
reconDist = signWidth - 85

class Common():
  # Function Opens an Image
  @staticmethod
  def open_image(path, bw):
    try:
      image = Image.open(path)

      if bw == 1:
        image = image.convert('1')  # convert image to black and white
      return image

    except IOError:
      return None

  # Function Saves Image
  @staticmethod
  def save_image(image, filepath):
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    print("({}) {} has been successfully exported!".format(st, filepath))
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    image.save(filepath, optimize=True, format="PNG")

  # function checks image dimension is a square;
  # yes - return resize image, no - return None
  @staticmethod
  def validate_resize_image(image):
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

  # this function checks if the client's
  # username given by the bank exists
  @staticmethod
  def user_exists(username):
    if User.query.filter_by(username=username).first() == None:
      return None
    else:
      return "OK"

  # get the banks this particular client subscribed
  @staticmethod
  def get_bank_usernames(client_userid):
    bank_subcribed = Client_Data.query.filter_by(client_userid=client_userid).all()

    usernames = []

    for bank in bank_subcribed:
      usernames.append(Common.userid_to_username(bank.getBankUserId()))

    return usernames

  # get all of the transactions of the bankID given
  @staticmethod
  def get_bank_transactions(bank_userid):
    pending_cheques = Transaction.query.filter_by(bank_userid=bank_userid).order_by(desc(Transaction.timestamp)).all()
    return pending_cheques

  # convert ID -> Username 
  @staticmethod
  def userid_to_username(userid):
    return User.query.filter_by(id=userid).first().getUsername() 

  # get email of the particular user
  @staticmethod
  def userid_to_useremail(userid):
    return User.query.filter_by(id=userid).first().getEmail() 