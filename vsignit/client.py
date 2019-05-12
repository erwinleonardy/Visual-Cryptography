# Filename: client.py
# Author: Erwin Leonardy
# Descrption: This file contains all of the necessary functions to operate the client page

import time, datetime, hashlib

from vsignit.common import Common, signCords
from vsignit.models import Transaction
from vsignit import db

class Client:
  def __init__(self, bankID, clientID, clientCheque, clientShare):
    self.bankID = bankID
    self.clientID = clientID
    self.cheque = clientCheque
    self.share = clientShare
    self.username = Common.userid_to_username(clientID)

    currentTime = time.time()
    self.timestamp = datetime.datetime.fromtimestamp(currentTime).strftime('%Y-%m-%d %H:%M:%S')

    hashed_ts = hashlib.sha1()
    namestamp = self.timestamp + " " + self.username
    hashed_ts.update(namestamp.encode('utf-8'))
    self.transactionNo = hashed_ts.hexdigest()
    self.filepath = './vsignit/output/cheque/cheque_' + self.transactionNo

  # Function pastes the source pic on top of the destination pic
  def signcheque(self):
    # resizes cheque to the intended size, no matter whatever size is given
    imageFormat = self.cheque.format
    self.cheque = Common.resizeImage(self.cheque, (2480, 1748))

    # extract background and store as an encrypted image for colored background
    crop_area = (signCords[0], signCords[1], signCords[0] + \
                self.share.width, signCords[1] + self.share.height)
    cheque_bg = self.cheque.crop(crop_area)
    bg_string = Common.encodeImage(cheque_bg, imageFormat)
    Common.encryptImage(bg_string, self.filepath + '_bg.png')

    # sign cheque
    self.cheque.paste(self.share, signCords) 

    # encrypt and save the file until transaction is complete
    cheque_string = Common.encodeImage(self.cheque, imageFormat)
    Common.encryptImage(cheque_string, self.filepath + '.png')

    return (cheque_string.decode("utf-8") + "," + self.username)

  # Function adds the transaction to the database 
  def store_transaction(self):
    newTransaction = Transaction(self.transactionNo, self.bankID, self.clientID, self.timestamp, self.filepath + '.png') 
    db.session.add(newTransaction)
    db.session.commit()

    return self.transactionNo, self.timestamp
