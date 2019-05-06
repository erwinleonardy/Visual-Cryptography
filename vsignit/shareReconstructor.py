# Filename: shareReconstructor.py
# Author: Erwin Leonardy
# Descrption: This file contains all of the necessary functions to reconstruct the shares

import PIL.ImageOps, base64, os
from PIL import Image

from vsignit.common import Common, signCords, B, W #signX, signY, signWidth, doubSignSize, reconDist
from vsignit.models import Transaction, Bank_Data
from vsignit import db

class ShareReconstructor():
  def __init__(self):
    pass

  # Function gets the client cheque from the database
  @staticmethod
  def get_client_cheque(transaction):
    transaction_no = transaction.getTranscationNo()
    chequePath = transaction.getFilePath()
    return transaction_no, Common.openImage(chequePath)

  # Function gets the bank share from the database
  @staticmethod
  def get_bank_share(transaction):
    bankID = transaction.getBankId()
    clientID = transaction.getClientId()

    bankSharePath = Bank_Data.query.filter_by(bank_userid=bankID, client_userid=clientID).first().getBankSharePath()
    return Common.openImage(bankSharePath)

  # Function removes the cheque image which bears the transaction number given
  @staticmethod
  def delete_cheque(transaction):
    chequeFilepath = transaction.getFilePath()
    # throws an error if file couldn't be found
    if not os.path.isfile(chequeFilepath):
      raise ValueError
    os.remove(chequeFilepath)
  
  # Function removes and temp. reconstructed images from the database
  @staticmethod
  def delete_transactionImages(transaction_no):
    reconCheque = "./vsignit/output/tmp/recon_cheque_" + transaction_no + ".png"
    reconFilepath = "./vsignit/output/tmp/recon_" + transaction_no + ".png"
    clean1Filepath = "./vsignit/output/tmp/clean1_" + transaction_no + ".png"
    clean2Filepath = "./vsignit/output/tmp/clean2_" + transaction_no + ".png"

    if os.path.isfile(reconCheque):
      os.remove(reconCheque)
    if os.path.isfile(reconFilepath):
      os.remove(reconFilepath)
    if os.path.isfile(clean1Filepath):
      os.remove(clean1Filepath)
    if os.path.isfile(clean2Filepath):
      os.remove(clean2Filepath)

  # Function removes the transaction record from the database
  @staticmethod
  def delete_transaction(transaction):
    db.session.delete(transaction)
    db.session.commit()

  # cleans reconstructed image to remove random noise
  def cleanSecret(self, secret):
    clean = Image.new('RGBA', secret.size)

    for x in range(0, secret.width, 2):
      for y in range(0, secret.height, 2):
        sum = secret.getpixel((x, y)) + secret.getpixel((x + 1, y)) + \
                secret.getpixel((x, y + 1)) + secret.getpixel((x + 1, y + 1))
        if (sum > 0):
          alpha = ((W,W,W,0), (W,W,W,0), (W,W,W,0), (W,W,W,0))
        else:
          alpha = ((B,B,B,255), (B,B,B,255), (B,B,B,255), (B,B,B,255))
          
        Common.placePixels(clean, alpha, (x, y))

    return clean

  def reconstructShares(self, bankShare, clientShare, transaction_no):
    bankShare.paste(clientShare, mask = bankShare)
    Common.save_image(bankShare, "./vsignit/output/tmp/recon_" + transaction_no + ".png")

    secret = self.cleanSecret(bankShare)
    Common.save_image(secret, "./vsignit/output/tmp/clean1_" + transaction_no + ".png")
    Common.save_image (secret, "./vsignit/output/tmp/clean2_" + transaction_no + ".png")
    return secret, bankShare

  def resetCheque(self, cheque, size, crop):
    white = Image.new('1', size, W)
    cheque.paste(white, crop)

  def reconstructCheque(self, bankShare, cheque, transaction_no):
    cropRegion = (signCords[0], signCords[1], signCords[0] + bankShare.width, signCords[1] + bankShare.height)
    clientShare = cheque.crop(cropRegion)
    clientShare = clientShare.convert('1')

    # checks if both of the shares have the same dimension
    if (clientShare.size != bankShare.size):
      return ""

    try:
      secret, clean1 = self.reconstructShares(bankShare, clientShare, transaction_no)
    except Exception:
      return ""

    self.resetCheque(cheque, clientShare.size, cropRegion)
    cheque.paste(secret, signCords, secret)
    Common.save_image(cheque, "./vsignit/output/tmp/recon_cheque_" + transaction_no + ".png")

    # send back all of the images back in BASE64 format
    # bankUsername = transaction.getBankUsername()
    # clientUsername = transaction.getClientUsername()

    with open("./vsignit/output/tmp/recon_cheque_" + transaction_no + ".png", "rb") as data:
      cheque = base64.b64encode(data.read())
    # data += ",".encode('utf-8')

    with open("./vsignit/output/tmp/clean1_" + transaction_no + ".png", "rb") as data:
      clean1 = base64.b64encode(data.read())

    with open("./vsignit/output/tmp/recon_" + transaction_no + ".png", "rb") as data:
      secret = base64.b64encode(data.read())

    # delete the temp files from the database
    ShareReconstructor.delete_transactionImages(transaction_no)
    
    return cheque.decode("utf-8"), clean1.decode("utf-8"), secret.decode("utf-8")