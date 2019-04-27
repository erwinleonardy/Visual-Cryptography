# Filename: client.py
# Author: Erwin Leonardy
# Descrption: This file contains all of the necessary functions to operate the client page

import os, time, datetime, base64, hashlib

from vsignit.common import Common, signX, signY
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