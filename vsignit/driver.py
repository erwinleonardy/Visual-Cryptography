# Filename: driver.py
# Author: Erwin Leonardy
# Descrption: This file contains all of the necessary functions to run the web application.

import re, time, base64, sys
from flask import url_for
from PIL import Image

from vsignit.shareReconstructor import ShareReconstructor
from vsignit.emailerService import EmailerService
from vsignit.shareSplitter import ShareSplitter
from vsignit.register import Register
from vsignit.client import Client
from vsignit.common import Common
from vsignit.login import Login

class Driver:
  # Function to register the user to the system
  @staticmethod
  def register(username, email, password, verification):
    user = Register(username, email, password, verification)
    return user.register()

  # Function to Login to the system
  @staticmethod
  def login(username, password):
    user = Login(username, password)
    if user.login():
      return url_for('index')
    else:
      return ""

  # Share Splitter Driver Function
  @staticmethod
  def create_shares(sigEncoded, username):
    if Common.user_exists(username) == None:
      return "No User"

    sigData = base64.b64decode(sigEncoded)
    sigImage = Common.openSecret(sigData)

    if Common.validate_resize_image(sigImage) == None:
      return "" 

    splitter = ShareSplitter(sigImage, username)
    shareStatus = splitter.createShares() #split into two shares
    return shareStatus

  # Client Page Driver Function
  @staticmethod
  def client_signcheque(clientID, bankID, chequeEncoded, client_share_db_path):
    # downloads the share from the cloud
    client_share_path = "./vsignit/output/" + client_share_db_path
    Common.downloadFromGoogle(client_share_db_path, client_share_path)

    # decodes the share
    client_share_token = Common.openEncrypted(client_share_path)
    client_share = Common.decryptImage(client_share_token)
    if client_share == None:
      return ""

    chequeData = base64.b64decode(chequeEncoded)
    clientCheque = Common.openEncoded(chequeData)
    client = Client(bankID, clientID, clientCheque, client_share)

    # adds this current transcation to the databsase
    transactionNo, timestamp = client.store_transaction()

    # sends an email notification to both bank and client
    EmailerService.signcheque_email(transactionNo, timestamp, bankID, clientID)
    
    # overlays the client share on top of the cheque
    result = client.signcheque()
    return result

  # Share Reconstruction Driver Function
  @staticmethod
  def reconstruct_shares(transaction):
    # retrieves the client cheque
    transactionNo, clientCheque = Common.get_client_cheque(transaction)
    
    # retrieves the bankShare
    bankShare = Common.get_bank_share(transaction)
    
    # reconstruct the shares based on the client cheque and bank share given
    reconstructor = ShareReconstructor(clientCheque, bankShare, transactionNo)
    reconCheque, cleanSig, reconSig = reconstructor.reconstructCheque()
 
    return reconCheque, cleanSig, reconSig

  # Function triggered during verification process
  # Success : Send successful email and delete transaction
  # Fail    : Send fail emails and delete transaction
  @staticmethod
  def transaction_verification(transaction, bank_response):
    transaction_no = transaction.getTranscationNo()
    client_userid = transaction.getClientId()
    bank_userid = transaction.getBankId()
    
    print("bank_response: " + bank_response)

    # checks users response
    # 'accept' -> Sends successful email to the client and bank
    # 'reject' -> sends fail email to the client and bank
    if bank_response == 'accept':
      EmailerService.transaction_email(transaction_no, client_userid, bank_userid, bank_response)
    else:
      EmailerService.transaction_email(transaction_no, client_userid,bank_userid, bank_response)

  # Function to delete the transaction from the DB
  @staticmethod
  def transaction_deletion(transaction):
    # rejection email
    EmailerService.transaction_email(transaction.getTranscationNo(), transaction.getClientId(), transaction.getBankId(), 'reject')
    Common.delete_cheque(transaction) # delete image
    Common.delete_transaction(transaction) # delete the share from the DB and remove the image
