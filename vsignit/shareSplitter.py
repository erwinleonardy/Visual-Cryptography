# Filename: shareSplitter.py
# Author: Erwin Leonardy
# Descrption: This file contains all of the necessary functions to split the shares

import random, os, secrets
from PIL import Image, ImageDraw, ImageFont
from flask_login import current_user

from vsignit.models import User, Client_Data, Bank_Data
from vsignit.common import Common, imageSize, B, W
from vsignit.emailerService import EmailerService
from vsignit import db, bucket

from google.cloud import storage

class ShareSplitter():
  def __init__(self, sigImage, username):
    self.sigImage = sigImage
    self.username = username

  # If both source1, source2 pixels are black
  def b1b2(self, hiddenColor):
    setA = ((W,B,B,B), (B,W,B,B), (B,B,W,B), (B,B,B,W))
    share1Pixel = random.choice(setA)
    
    # IF secret pixel is black: set share pixels with 3 black pixels each, 
    # such that when they overlap they form a set of 4 black pixels
    # ELIF secret pixel is white: set both share pixels with 3 of the same black pixels
    if (hiddenColor == B):
      share2Pixel = share1Pixel
      # as long as the set of 4 subpixels are not the same, condition is met
      while (share1Pixel == share2Pixel):
        share2Pixel = random.choice(setA)
    elif (hiddenColor == W):
      share2Pixel = share1Pixel

    return (share1Pixel, share2Pixel)

  # If one source pixel is black, and the other white
  def b1w2(self, hiddenColor):
    # IF secret pixel is black: source with black pixel will have 3 black pixels
    # while source with white pixel will have 2 black pixels, when overlapped they should
    # form a set of 4 black pixels
    # ELIF secret pixel is white: same as black, but when overlapped they should form a set
    # of 3 black pixels
    if (hiddenColor == B):
      share1Pixel = [B,B,B,B]
      share2Pixel = [W,W,W,W]

      blackOne = random.randint(0,3)
      share1Pixel[blackOne] = W # remove 1 random black pixel from share1
      blackTwo = blackOne
      while (blackTwo == blackOne):
        blackTwo = random.randint(0,3)

      share2Pixel[blackOne] = B # set overlapping black pixel
      share2Pixel[blackTwo] = B # set black pixel to meet condition

      share1Pixel = tuple(share1Pixel)
      share2Pixel = tuple(share2Pixel)
    elif (hiddenColor == W):
      setA = ((W,B,B,B), (B,W,B,B), (B,B,W,B), (B,B,B,W))
      share1Pixel = random.choice(setA)
      share2Pixel = list(share1Pixel)
      i_B = 0 # location of black pixel to remove
      for i in range(len(share2Pixel)):
        if (share2Pixel[i] == B):
          i_B = i

      share2Pixel[i_B] = W # remove a black pixel
      share2Pixel = tuple(share2Pixel)

    return (share1Pixel, share2Pixel)

  # If both source1, source2 pixels are white
  def w1w2(self, hiddenColor):
    setA = ((W,W,B,B), (B,B,W,W), (W,B,W,B), (B,W,B,W), (W,B,B,W), (B,W,W,B))
    share1Pixel = random.choice(setA)

    # IF secret pixel is black: both shares will have 2 black subpixels each, such that when
    # overlapped they form 4 black pixels
    # ELIF secret pixel is white: same as above, but when overlapped they should form a set
    # of 3 black pixels
    if (hiddenColor == B):
      share2Pixel = [B,B,B,B]
      # share2Pixels are opposite of share1Pixels
      for i in range(len(share1Pixel)):
        if (share1Pixel[i] == B):
          share2Pixel[i] = W
      
      share2Pixel = tuple(share2Pixel)
    elif (hiddenColor == W):
      share2Pixel = list(share1Pixel)
      i_B = 0 
      i_W = 0
      for i in range(len(share2Pixel)):
        if (share2Pixel[i] == B):
          i_B = i
        else:
          i_W = i

      share2Pixel[i_B] = W # a black pixel is replaced
      share2Pixel[i_W] = B # a white pixel is replaced
      share2Pixel = tuple(share2Pixel)

    return (share1Pixel, share2Pixel)

  # sets the subpixels within shares
  def placePixels(self, share, tup, cords):
    x, y = cords[0], cords[1]

    share.putpixel((x, y), tup[0])
    share.putpixel((x + 1, y), tup[1])
    share.putpixel((x, y + 1), tup[2])
    share.putpixel((x + 1, y + 1), tup[3])

  # based on the pixel colors from hidden, source1, source2,
  # set the subpixels of the two new shares
  def setSharePixels(self, hidden, source1, source2, share1, share2, cords):
    # get pixel color for the following, each either black or white
    hiddenPxl = hidden.getpixel(cords)
    source1Pxl = source1.getpixel(cords)
    source2Pxl = source2.getpixel(cords)

    # 4 possible combinations of source1, source2 pixel color,
    # each case results in a different set of subpixels in shares
    if (source1Pxl == B and source2Pxl == B):
      subPixels = self.b1b2(hiddenPxl)
    elif (source1Pxl == B and source2Pxl == W):
      subPixels = self.b1w2(hiddenPxl)
    elif (source1Pxl == W and source2Pxl == B):
      subPixels = self.b1w2(hiddenPxl)
      share1, share2 = share2, share1
    elif (source1Pxl == W and source2Pxl == W):
      subPixels = self.w1w2(hiddenPxl)

    subCords = (cords[0] * 2, cords[1] * 2)
    self.placePixels(share1, subPixels[0], subCords)
    self.placePixels(share2, subPixels[1], subCords)

  # create source images
  def createSource(self, size):
    choice = (W, B)
    color = random.choice(choice)

    img = Image.new('1', size, color)
    font = ImageFont.truetype("vsignit/font/BebasNeue-Regular.ttf", 78)
    word = secrets.token_urlsafe(3)
    wordSize = font.getsize(word)
    cords = ((img.width - wordSize[0])//2,(img.height - wordSize[1])//2)

    draw = ImageDraw.Draw(img)
    draw.text(cords, word, (255 - color), font)
    return img

  # creates two new shares based on three images provided
  def createShares(self):
    # resize image to fit on cheque after reconstruction
    if (self.sigImage.size != imageSize):
      self.sigImage = Common.resizeImage(self.sigImage)
      
    # create source images to base shares off
    source1 = self.createSource(self.sigImage.size)
    source2 = self.createSource(self.sigImage.size)

    # create new images for manipulation
    share1 = Image.new('1', (source1.width*2, source1.height*2))
    share2 = Image.new('1', (source1.width*2, source1.height*2))

    # x is horizontal, y is vertical; start from (0,0) 
    for x in range(self.sigImage.width):
      for y in range(self.sigImage.height):
        cords = (x, y) # pixel coordinates
        self.setSharePixels(self.sigImage, source1, source2, share1, share2, cords)

    signStatus = self.store_shares(share1, share2)
    return signStatus

  # Function sends client/bank shares to respective emails
  def store_shares(self, share1, share2):
    bank_userid = current_user.get_id()
    client_userid = User.query.filter_by(username=self.username).first().id
    bank_username = User.query.filter_by(id=bank_userid).first().username

    # exports and encrypts image shares
    bank_share_path = "./vsignit/output/bank/" + self.username + "_" + bank_username + "_bank_share.png"
    client_share_path = "./vsignit/output/client/" + self.username + "_" + bank_username + "_client_share.png"
    bank_share_db_path = "bank/" + self.username + "_" + bank_username + "_bank_share.png"
    client_share_db_path = "client/" + self.username + "_" + bank_username + "_client_share.png"

    bank_share_string = Common.encodeImage(share1, "PNG")
    Common.encryptImage(bank_share_string, bank_share_path)

    client_share_string = Common.encodeImage(share2, "PNG")
    Common.encryptImage(client_share_string, client_share_path)

    # uploads to cloud
    Common.uploadToGoogle(bank_share_path, bank_share_db_path)
    Common.uploadToGoogle(client_share_path, client_share_db_path)

    # deletes the share
    os.remove(bank_share_path)
    os.remove(client_share_path)

    # checks if data already exists
    existingBank = Bank_Data.query.get([bank_userid, client_userid])
    existingClient = Client_Data.query.get([client_userid, bank_userid])

    # if yes, overwrites it
    if existingBank != None and existingClient != None:
      existingBank.bank_share_path = bank_share_db_path
      existingClient.client_share_path = client_share_db_path 
      db.session.commit()     
      return "You have just overwritten \'" + self.username + "\' client and bank shares!"

    # else, creates a new record
    else:     
      newBankData = Bank_Data(bank_userid, client_userid, bank_share_db_path)
      newClientData = Client_Data(client_userid, bank_userid, client_share_db_path)
      db.session.add(newBankData)
      db.session.add(newClientData)
      db.session.commit()
      return "Bank share and user shares have been created and stored!"