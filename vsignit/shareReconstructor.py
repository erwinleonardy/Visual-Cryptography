# Filename: shareReconstructor.py
# Author: Erwin Leonardy
# Descrption: This file contains all of the necessary functions to reconstruct the shares

import PIL.ImageOps, base64, os
from PIL import Image

from vsignit.common import signX, signY, signWidth, doubSignSize, reconDist
from vsignit.models import Transaction, Bank_Data
from vsignit.common import Common
from vsignit import db

class ShareReconstuctor():
  # Function gets the client cheque from the database
  @staticmethod
  def get_client_cheque(transaction):
    transaction_no = transaction.getTranscationNo()
    chequePath = transaction.getFilePath()
    return transaction_no, Common.open_image(chequePath, 1)

  # Function gets the bank share from the database
  @staticmethod
  def get_bank_share(transaction):
    bankID = transaction.getBankId()
    clientID = transaction.getClientId()

    bankSharePath = Bank_Data.query.filter_by(bank_userid=bankID, client_userid=clientID).first().getBankSharePath()
    return Common.open_image(bankSharePath, 1)

  # Function overlays the picture and preserves its transparency
  @staticmethod
  def overlay_pic(transaction_no, sourcepath, dest):
    source = Image.open(sourcepath)
    dest.paste(source, (signX+reconDist, signY+(reconDist*2)), mask=source)       
    Common.save_image (dest, "./vsignit/output/tmp/recon_cheque_" + transaction_no + ".png")   

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
  def delete_transactionImages(transaction):
    reconCheque = "./vsignit/output/tmp/recon_cheque_" + transaction.getTranscationNo() + ".png"
    reconFilepath = "./vsignit/output/tmp/recon_" + transaction.getTranscationNo() + ".png"
    clean1Filepath = "./vsignit/output/tmp/clean1_" + transaction.getTranscationNo() + ".png"
    clean2Filepath = "./vsignit/output/tmp/clean2_" + transaction.getTranscationNo() + ".png"

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

  # Function reconstructs the image using two of the shares
  @staticmethod
  def reconstruct_shares(transaction_no, clientCheque, bankShare):
    bankWidth, bankHeight = bankShare.size
    signWidth = int(bankWidth / 2)
    doubSignSize = signWidth * 2

    if clientCheque == None:
      return ""

    # extract the shares area
    clientShare = clientCheque.crop((signX, signY, signX+(doubSignSize), signY+(doubSignSize)))
    clientShare.thumbnail((doubSignSize, doubSignSize), Image.ANTIALIAS)
    clientShare = clientShare.convert('1')
    clientWidth, clientHeight = clientShare.size

    # checks if both of the shares have the same dimension
    if (bankWidth == clientWidth and bankHeight == clientHeight): 
        try:
            # reconstruct the shares
            outfile = Image.new('1', clientShare.size)

            for x in range(clientShare.size[0]):
                for y in range(clientShare.size[1]): 
                    outfile.putpixel((x,y), min(clientShare.getpixel((x, y)), bankShare.getpixel((x, y))))

            Common.save_image (outfile, "./vsignit/output/tmp/recon_" + transaction_no + ".png")    

            return outfile
        
        except IndexError:
            return ""

    # if no, return null (error)
    else:
        return ""

  # Function resizes the reconstructed image and clean the noise
  @staticmethod
  def remove_noise(transaction_no, inputImg):
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

    Common.save_image (outfile, "./vsignit/output/tmp/clean1_" + transaction_no + ".png")

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

    Common.save_image (image_trans, "./vsignit/output/tmp/clean2_" + transaction_no + ".png")

    return outfile

  # Function will allow the bank's share to be downloaded
  @staticmethod
  def get_reconstructed(transaction, clientCheque, outfile):
    # replace the area with white color
    for x in range(signX, signX+(doubSignSize)):
        for y in range(signY, signY+(doubSignSize)):
            clientCheque.putpixel((x, y), 255)

    # place the clean shares to it
    transaction_no = transaction.getTranscationNo()
    ShareReconstuctor.overlay_pic(transaction_no, "./vsignit/output/tmp/clean2_" + transaction_no + ".png", clientCheque)

    # send back all of the images back in BASE64 format
    bankUsername = transaction.getBankUsername()
    clientUsername = transaction.getClientUsername()

    with open("./vsignit/output/tmp/recon_cheque_" + transaction_no + ".png", "rb") as data:
      recon_cheque = base64.b64encode(data.read())
    # data += ",".encode('utf-8')

    with open("./vsignit/output/tmp/clean1_" + transaction_no + ".png", "rb") as data:
      clean1 = base64.b64encode(data.read())

    with open("./vsignit/output/tmp/recon_" + transaction_no + ".png", "rb") as data:
      recon = base64.b64encode(data.read())

    # delete the temp files from the database
    ShareReconstuctor.delete_transactionImages(transaction)

    return recon_cheque.decode("utf-8"), clean1.decode("utf-8"), recon.decode("utf-8")