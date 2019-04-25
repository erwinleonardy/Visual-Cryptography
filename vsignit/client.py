# Filename: client.py
# Author: Erwin Leonardy
# Descrption: This file contains all of the necessary functions to operate the client page

import os, time, datetime, base64, hashlib

from vsignit.common import Common, signX, signY
from vsignit.emailerService import EmailerService
from vsignit.models import Transaction
from vsignit import db

class Client:
  # Function adds the transaction to the database
  @staticmethod 
  def store_transaction(bank_userid, client_userid):
    clientUsername = Common.userid_to_username(client_userid)

    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    conct = st + " " + clientUsername

    hashed_ts = hashlib.sha1()
    hashed_ts.update(conct.encode('utf-8'))
    filepath = "./vsignit/output/cheque/cheque_" + hashed_ts.hexdigest() + ".png"

    newTransaction = Transaction(hashed_ts.hexdigest(), bank_userid, client_userid, st, filepath) 
    db.session.add(newTransaction)
    db.session.commit()

    return hashed_ts.hexdigest(), st, filepath

  # Function sends confirmation email to client and server
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

  # Function pastes the source pic on top of the destination pic
  @staticmethod
  def signcheque(client_share, client_cheque, filepath, client_username):
    client_cheque.paste (client_share,(signX, signY))   

    # save the file temporarily
    Common.save_image (client_cheque, filepath)      

    # export the image to base64 format
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())

    return (encoded_string.decode("utf-8") + "," + client_username)