"""
    shareReconstructor.py
    by: Erwin Leonardy

    This file contains all of the necessary
    functions to reconstruct the shares
"""

from PIL import Image
import PIL.ImageOps
import base64, os

from vsignit import db
from vsignit.common import Common
from vsignit.common import signX, signY, signWidth, doubSignSize, reconDist
from vsignit.models import Transaction, Bank_Data
from vsignit.emailerService import EmailerService

class ShareReconstuctor():
    
    """
        This function gets the client cheque
        from the database
    """
    @staticmethod
    def getClientCheque (transaction):
      transactionNo = transaction.getTranscationNo()
      chequePath = transaction.getFilePath()
      return transactionNo, Common.open_image(chequePath, 1)

    """
        This function gets the bank share
        from the database
    """
    @staticmethod
    def getBankShare (transaction):
      bankID = transaction.getBankId()
      clientID = transaction.getClientId()

      bankSharePath = Bank_Data.query.filter_by(bank_userid=bankID, client_userid=clientID).first().getBankSharePath()
      return Common.open_image(bankSharePath, 1)

    """ 
        This function overlays the picture and
        it preserves the transparency
    """
    @staticmethod
    def overlay_pic (transactionNo, sourcePath, dest):
      source = Image.open(sourcePath)
      dest.paste(source, (signX+reconDist, signY+(reconDist*2)), mask=source)       
      Common.save_image (dest, "./vsignit/output/tmp/recon_cheque_" + transactionNo + ".png")   

    """
        This function removes the cheque image which 
        bears the transaction number given
    """
    @staticmethod
    def delete_cheque (transaction):
      filepath = transaction.getFilePath()
      os.remove(filepath)

    """
        This function removes the transaction record
        from the databse
    """
    @staticmethod
    def delete_transaction (transaction):
      db.session.delete(transaction)
      db.session.commit()

    """
        This function reconstructs the image 
        using two of the shares
    """
    @staticmethod
    def reconstruct_shares (transactionNo, clientCheque, bankShare):
      bankWidth, bankHeight = bankShare.size
      signWidth = int(bankWidth / 2)
      doubSignSize = signWidth * 2

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

              Common.save_image (outfile, "./vsignit/output/tmp/recon_" + transactionNo + ".png")    

              return outfile
          
          except IndexError:
              return ""

      # if no, return null (error)
      else:
          return ""

    """
        This function resizes the reconstructed 
        image and clean the noise
    """
    @staticmethod
    def remove_noise (transactionNo, inputImg):
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

      Common.save_image (outfile, "./vsignit/output/tmp/clean1_" + transactionNo + ".png")
  
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

      Common.save_image (image_trans, "./vsignit/output/tmp/clean2_" + transactionNo + ".png")

      return outfile

    """
        This function will allow the bank's share 
        to be downloaded
    """
    @staticmethod
    def get_reconstructed (transaction, clientCheque, outfile):
      # replace the area with white color
      for x in range(signX, signX+(doubSignSize)):
          for y in range(signY, signY+(doubSignSize)):
              clientCheque.putpixel((x, y), 255)

      # place the clean shares to it
      transactionNo = transaction.getTranscationNo()
      ShareReconstuctor.overlay_pic(transactionNo, "./vsignit/output/tmp/clean2_" + transactionNo + ".png", clientCheque)

      # send back all of the images back in BASE64 format
      bankUsername = transaction.getBankUsername()
      clientUsername = transaction.getClientUsername()

      with open("./vsignit/output/tmp/recon_cheque_" + transactionNo + ".png", "rb") as data:
        recon_cheque = base64.b64encode(data.read())
      # data += ",".encode('utf-8')

      with open("./vsignit/output/tmp/clean1_" + transactionNo + ".png", "rb") as data:
        clean1 = base64.b64encode(data.read())

      with open("./vsignit/output/tmp/recon_" + transactionNo + ".png", "rb") as data:
        recon = base64.b64encode(data.read())

      return recon_cheque.decode("utf-8"), clean1.decode("utf-8"), recon.decode("utf-8")

    """
        This function is send successful email to the bank and client
    """
    @staticmethod
    def emailAccept (transaction_no, client_userid, bank_userid):
      clientUsername = Common.getUsernameFromID(client_userid)
      bankUsername = Common.getUsernameFromID(bank_userid)
      bank_email = Common.getUserEmail(bank_userid)
      client_email = Common.getUserEmail(client_userid)

      # send email to bank
      bankSubject = "({}) Outcome of Cheque {}".format(bankUsername, transaction_no)
      bankMessage = """
      You have have just decided to accept a cheque from {}.

      Transaction Number: {}""".format(clientUsername, transaction_no)
      EmailerService.sendEmail(bankUsername, bank_email, bankSubject, bankMessage)

      # send email to client
      clientSubject = "({}) Outcome of Cheque {}".format(clientUsername, transaction_no)
      clientMessage = """
      Hooray! {} have just decided to accept your cheque.

      Transaction Number: {}
      
      Please do call your bank hotline if you have further enquiries.""".format(bankUsername, transaction_no)
      EmailerService.sendEmail(clientUsername, client_email, clientSubject, clientMessage)
      

    """
        This function is send fail email to the bank and client
    """
    @staticmethod
    def emailReject (transaction_no, client_userid, bank_userid):
      clientUsername = Common.getUsernameFromID(client_userid)
      bankUsername = Common.getUsernameFromID(bank_userid)
      bank_email = Common.getUserEmail(bank_userid)
      client_email = Common.getUserEmail(client_userid)

      # send email to bank
      bankSubject = "({}) Outcome of Cheque {}".format(bankUsername, transaction_no)
      bankMessage = """
      You have have just decided to reject a cheque from {}.

      Transaction Number: {}""".format(clientUsername, transaction_no)
      EmailerService.sendEmail(bankUsername, bank_email, bankSubject, bankMessage)

      # send email to client
      clientSubject = "({}) Outcome of Cheque {}".format(clientUsername, transaction_no)
      clientMessage = """
      {} have just decided to reject your cheque.

      Transaction Number: {}
      
      Please do call your bank hotline if you think something has gone amiss.""".format(bankUsername, transaction_no)
      EmailerService.sendEmail(clientUsername, client_email, clientSubject, clientMessage)

        