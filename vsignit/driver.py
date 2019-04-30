# Filename: driver.py
# Author: Erwin Leonardy
# Descrption: This file contains all of the necessary functions to run the web application.

from __future__ import print_function
import PIL.ImageOps, re, time, base64, sys, os
from flask import url_for
from PIL import Image

from vsignit.shareReconstructor import ShareReconstuctor
from vsignit.shareSplitter import ShareSplitter
from vsignit.register import Register
from vsignit.common import Common
from vsignit.client import Client
from vsignit.login import Login

class Driver():
  # Function to Login to the system
  @staticmethod
  def login(username, password):
    if Login.login(username, password):
      return url_for('index')
    else:
      return ""

  # Function to register the user to the system
  @staticmethod
  def register(username, email, password, verification):
    return Register.register(username, email, password, verification)

  # Share Splitter Driver Function
  @staticmethod
  def create_shares(image, username):
    # checks if the username exists
    if Common.user_exists(username) == None:
      return "No User"

    # resize the image
    image = ShareSplitter.resize(image)

    # split into two shares
    outfile1, outfile2 = ShareSplitter.create_shares(image)

    # send the shares to the 
    encoded_str = ShareSplitter.store_shares(outfile1, outfile2, username)

    return encoded_str

  # Share Reconstruction Driver Function
  @staticmethod
  def reconstruct_shares(transaction):
    # retrieves the client cheque
    transactionNo, clientCheque = ShareReconstuctor.get_client_cheque(transaction)

    # retrieves the bankShare
    bankShare = ShareReconstuctor.get_bank_share(transaction)
    
    # reconstruct the shares based on the client cheque and bank share given
    outfile = ShareReconstuctor.reconstruct_shares(transactionNo, clientCheque, bankShare)
    
    # if error occurs, it will return None
    if outfile == "":
      return ""

    # else, proceed
    else:
      # pass through 2 cleaning processes
      outfile = ShareReconstuctor.remove_noise(transactionNo, outfile)

      # send the reconstructed shares to the client
      recon_cheque, clean1, recon = ShareReconstuctor.get_reconstructed(transaction, clientCheque, outfile)

      return recon_cheque, clean1, recon

  # Function triggered during verification process
  # Success : Send successful email and delete transaction
  # Fail    : Send fail emails and delete transaction
  @staticmethod
  def transaction_verification(transaction, bank_response):
    transaction_no = transaction.getTranscationNo()
    client_userid = transaction.getClientId()
    bank_userid = transaction.getBankId()
    
    # checks users response
    # 'accept' -> Sends successful email to the client and bank
    # 'reject' -> sends fail email to the client and bank
    if bank_response == 'accept':
      Common.transaction_email(transaction_no, client_userid, bank_userid, bank_response)

    else:
      Common.transaction_email(transaction_no, client_userid,bank_userid, bank_response)

  # Function to delete the transaction from the DB
  @staticmethod
  def transaction_deletion(transaction):
    # delete existing image
    ShareReconstuctor.delete_cheque (transaction)

    # send rejection email
    Common.transaction_email(transaction.getTranscationNo(), transaction.getClientId(), transaction.getBankId(), 'reject')

    # delete the share from the DB and remove the image
    ShareReconstuctor.delete_transaction(transaction)
    ShareReconstuctor.delete_transactionImages(transaction)

  # Client Page Driver Function
  @staticmethod
  def client_signcheque(client_share, client_cheque, client_userid, bank_userid):
    # get the client's username based on the id
    clientUsername = Common.userid_to_username(client_userid)

    # adds this current transcation to the databsase
    transactionNo, timestamp, filepath = Client.store_transaction (bank_userid, client_userid)

    # sends an email notification to both bank and client
    Common.signcheque_email (transactionNo, timestamp, bank_userid, client_userid)

    # overlays the client share on top of the cheque
    result = Client.signcheque (client_share, client_cheque, filepath, clientUsername)

    return result