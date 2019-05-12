# Filename: common.py
# Author: Erwin Leonardy
# Descrption: This file contains all of the supporting functions that are shared across the 
#             other python files

import os, time, datetime, base64
from cryptography.fernet import Fernet
from sqlalchemy import desc
from io import BytesIO
from PIL import Image

from vsignit.models import User, Client_Data, Transaction, Bank_Data
from vsignit import db

B = 0
W = 255
signCords = (1750, 750)
imageSize = (200, 200)
shareSize = (imageSize[0] * 2, imageSize[1] * 2)

class Common():
  # this function checks if the client's username given by the bank exists
  # return: None if doesn't exist
  @staticmethod
  def user_exists(username):
    return None if User.query.filter_by(username=username).first() == None else "OK"

  # this function checks if the client's email given by the client exists
  # return: None if doesn't exist
  @staticmethod
  def email_exists(email):
    return None if User.query.filter_by(email=email).first() == None else "OK"

  # convert ID -> Username 
  @staticmethod
  def userid_to_username(userid):
    return User.query.filter_by(id=userid).first().getUsername() 

  # get email of the particular user
  @staticmethod
  def userid_to_useremail(userid):
    return User.query.filter_by(id=userid).first().getEmail() 

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

  # Function gets the bank share from the database
  @staticmethod
  def get_bank_share(transaction):
    bankID = transaction.getBankId()
    clientID = transaction.getClientId()
    bankSharePath = Bank_Data.query.filter_by(bank_userid=bankID, client_userid=clientID).first().getBankSharePath()
    return Common.openImage(bankSharePath)

  # Function gets the client cheque from the database
  @staticmethod
  def get_client_cheque(transaction):
    transaction_no = transaction.getTranscationNo()
    chequePath = transaction.getFilePath()
    # throws an error if file couldn't be found
    if not os.path.isfile(chequePath):
      raise ValueError
    token = Common.openEncrypted(chequePath)
    cheque = Common.decryptImage(token)
    return transaction_no, cheque

  # Function removes the transaction record from the database
  @staticmethod
  def delete_transaction(transaction):
    db.session.delete(transaction)
    db.session.commit()

  # Function removes the cheque image which bears the transaction number given
  @staticmethod
  def delete_cheque(transaction):
    chequeFilepath = transaction.getFilePath()
    bgpath = chequeFilepath[:-4] + '_bg.png'
    # throws an error if file couldn't be found
    if not os.path.isfile(chequeFilepath):
      raise ValueError
    os.remove(chequeFilepath)
    os.remove(bgpath)

  # converts a normal image to pure black.white pixels
  # RGB converted to B/W based on which color they are closer to
  @staticmethod
  def convertSecretToBlack(img):
    img = img.convert('RGB')
    image = Image.new('1', img.size)

    # replace all pixels with either black or white pixels
    # if RGB values are closer to white, replace with white, else black
    for x in range(img.width):
      for y in range(img.height):
        tup = img.getpixel((x,y))
        if (tup[0] > 175 and tup[1] > 175 and tup[1] > 175):
          image.putpixel((x,y), W)
        else:
          image.putpixel((x,y), B)

    return image

  # open shares safely
  @staticmethod
  def openImage(filename):
    return Image.open(filename)

  @staticmethod
  def openEncoded(encodedImage):
    return Image.open(BytesIO(encodedImage))

  @staticmethod
  def openEncrypted(filename):
    with open(filename, 'rb') as imageFile:
      return imageFile.read()

  @staticmethod
  def openSecret(secretEncoded):
    img = Image.open(BytesIO(secretEncoded))
    img = Common.convertSecretToBlack(img)
    return img

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
        image.resize(imageSize)
        img_w, img_h = image.size
        background = Image.new('1', imageSize, 255)
        bg_w, bg_h = background.size
        offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)
        background.paste(image, offset)
        return image
      except IOError:
        return None

  # Function resizes to the desired dimension (200 x 200)
  # if second argument is not provided
  @staticmethod
  def resizeImage(image, resultSize=imageSize):
    return image.resize(resultSize)

  @staticmethod
  def encryptImage(imageEncoded, savepath):
    f = Fernet('HdcT0QsyPAA5M-g9Ozk_RBlRUuo8eq8lS8DPix4d5z4=')
    os.makedirs(os.path.dirname(savepath), exist_ok=True)
    token = f.encrypt(imageEncoded)
    outfile = open(savepath, 'wb')
    outfile.write(token)
    outfile.close()

  @staticmethod
  def decryptImage(token):
    f = Fernet('HdcT0QsyPAA5M-g9Ozk_RBlRUuo8eq8lS8DPix4d5z4=')
    imageEncoded = f.decrypt(token)
    imageData = base64.b64decode(imageEncoded)
    image = Image.open(BytesIO(imageData))
    return image

  @staticmethod
  def encodeImage(image, format):
    buffer = BytesIO()
    image.save(buffer, format=format)
    string = base64.b64encode(buffer.getvalue())
    return string
