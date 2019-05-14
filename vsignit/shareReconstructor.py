# Filename: shareReconstructor.py
# Author: Erwin Leonardy
# Descrption: This file contains all of the necessary functions to reconstruct the shares

from PIL import Image

from vsignit.common import Common, signCords, B, W

class ShareReconstructor:
  def __init__(self, cheque, bankShare, transactionNo):
    self.cropRegion = (signCords[0], signCords[1], signCords[0] + bankShare.width, signCords[1] + bankShare.height)
    self.clientShare = cheque.crop(self.cropRegion)
    self.clientShare = self.clientShare.convert('1')

    self.bankShare = bankShare
    self.transactionNo = transactionNo
    self.cheque = cheque

  # sets the subpixels within shares
  def placePixels(self, share, tup, cords):
    x, y = cords[0], cords[1]

    share.putpixel((x, y), tup[0])
    share.putpixel((x + 1, y), tup[1])
    share.putpixel((x, y + 1), tup[2])
    share.putpixel((x + 1, y + 1), tup[3])

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
          
        self.placePixels(clean, alpha, (x, y))

    return clean

  def reconstructShares(self):
    secret = self.bankShare.copy()
    secret.paste(self.clientShare, mask=secret)

    clean = self.cleanSecret(secret)
    return clean, secret

  def resetCheque(self):
    # downloads cheque bg from Google
    cheque_bg_db_path = 'cheque/cheque_' + self.transactionNo + '_bg.png'
    cheque_bg_path = './vsignit/output/' + cheque_bg_db_path
    Common.downloadFromGoogle(cheque_bg_db_path, cheque_bg_path)

    # reconstruct bg
    bg_token = Common.openEncrypted(cheque_bg_path)
    bg = Common.decryptImage(bg_token)
    self.cheque.paste(bg, self.cropRegion)

  def reconstructCheque(self):
    # checks if both of the shares have the same dimension
    if (self.clientShare.size != self.bankShare.size):
      return ""

    try:
      clean, secret = self.reconstructShares()
    except Exception:
      return ""
   
    self.resetCheque()
    self.cheque.paste(clean, signCords, clean)

    cheque_string = Common.encodeImage(self.cheque, self.cheque.format)
    secret_string = Common.encodeImage(secret, self.bankShare.format)
    clean_string = Common.encodeImage(clean, self.bankShare.format)

    return cheque_string.decode("utf-8"), clean_string.decode("utf-8"), secret_string.decode("utf-8")