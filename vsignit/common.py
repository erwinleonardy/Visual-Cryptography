# Filename: common.py
# Author: Erwin Leonardy
# Descrption: This file contains all of the supporting functions that are shared across the 
#             other python files

import PIL.ImageOps, os, time, datetime, base64
from cryptography.fernet import Fernet, InvalidToken
from sqlalchemy import desc
from io import BytesIO
from PIL import Image

from vsignit.models import User, Client_Data, Transaction
from vsignit.emailerService import EmailerService

B = 0
W = 255
signCords = (1750, 750)
imageSize = (200, 200)
shareSize = (imageSize[0] * 2, imageSize[1] * 2)

class Common():
  @staticmethod
  def encryptImage(imageEncoded, savepath):
    f = Fernet(os.environ['CHEQUE_KEY'])

    os.makedirs(os.path.dirname(savepath), exist_ok=True)
    token = f.encrypt(imageEncoded)
    outfile = open(savepath, 'wb')
    outfile.write(token)
    outfile.close()

  @staticmethod
  def decryptImage(token):
    f = Fernet(os.environ['CHEQUE_KEY'])

    imageEncoded = f.decrypt(token)
    imageData = base64.b64decode(imageEncoded)
    image = Image.open(BytesIO(imageData))
    return image

  @staticmethod
  def openEncrypted(filename):
    with open(filename, 'rb') as imageFile:
      return imageFile.read()

  # Function resizes to the desired dimension (200 x 200)
  @staticmethod
  def resize(image):
    return image.resize(imageSize)

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

  # Open a normal image from filepath
  @staticmethod
  def openSecret(filename):
    try:
      img = Image.open(filename)
      img = Common.convertSecretToBlack(img)
      return img
    except IOError:
      return None

  # open shares safely
  @staticmethod
  def openImage(filename):
    try:
      img = Image.open(filename)
      return img
    except IOError:
      return None

  # sets the subpixels within shares
  @staticmethod
  def placePixels(share, tup, cords):
    x, y = cords[0], cords[1]

    share.putpixel((x, y), tup[0])
    share.putpixel((x + 1, y), tup[1])
    share.putpixel((x, y + 1), tup[2])
    share.putpixel((x + 1, y + 1), tup[3])

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

  # function to send email when cheque has been signed by client
  @staticmethod
  def signcheque_email(transaction_no, timestamp, bank_userid, client_userid):
    clientUsername = Common.userid_to_username(client_userid)
    bankUsername = Common.userid_to_username(bank_userid)
    bank_email = Common.userid_to_useremail(bank_userid)
    client_email = Common.userid_to_useremail(client_userid)

    # send email to bank
    bankSubject = "({}) New Cheque from {}".format(bankUsername, clientUsername)
    bankMessage = """
    You have received a new cheque to be processed from {}.

    Transaction Number: {}
    Transaction Time: {}""".format(clientUsername, transaction_no, timestamp)
    EmailerService.send_email(bankUsername, bank_email, bankSubject, bankMessage)

    # send email to client
    clientSubject = "({}) Your cheque has been sent to {}".format(clientUsername, bankUsername)
    clientMessage = """
    Your cheque is currently being processed by {}.

    Transaction Number: {}
    Transaction Time: {}
    
    Your bank will contact you should they have any issue.""".format(bankUsername, transaction_no, timestamp)
    EmailerService.send_email(clientUsername, client_email, clientSubject, clientMessage)
  
  # function to send email after bank determines what to do 
  # with cheque transaction
  @staticmethod
  def transaction_email(transaction_no, client_userid, bank_userid, bank_response):
    clientUsername = Common.userid_to_username(client_userid)
    bankUsername = Common.userid_to_username(bank_userid)
    bank_email = Common.userid_to_useremail(bank_userid)
    client_email = Common.userid_to_useremail(client_userid)

    # send email to bank
    bankSubject = "({}) Outcome of Cheque {}".format(bankUsername, transaction_no)
    bankMessage = """
    You have have just decided to {} a cheque from {}.

    Transaction Number: {}""".format(bank_response, clientUsername, transaction_no)
    EmailerService.send_email(bankUsername, bank_email, bankSubject, bankMessage)

    # send email to client
    clientSubject = "({}) Outcome of Cheque {}".format(clientUsername, transaction_no)
    clientMessage = """
    {} have just decided to {} your cheque.

    Transaction Number: {}
    
    Please do call your bank hotline if you have further enquiries.""".format(bankUsername, bank_response, transaction_no)
    EmailerService.send_email(clientUsername, client_email, clientSubject, clientMessage)

  # this function checks if the client's
  # username given by the bank exists
  # return: None if doesn't exist
  @staticmethod
  def user_exists(username):
    return None if User.query.filter_by(username=username).first() == None else "OK"

  # this function checks if the client's
  # email given by the client exists
  # return: None if doesn't exist
  @staticmethod
  def email_exists(email):
    return None if User.query.filter_by(email=email).first() == None else "OK"

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