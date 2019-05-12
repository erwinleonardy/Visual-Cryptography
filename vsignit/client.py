# Filename: client.py
# Author: Erwin Leonardy
# Descrption: This file contains all of the necessary functions to operate the client page

import os, time, datetime, base64, hashlib
from io import BytesIO

from vsignit.common import Common, signCords
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
    filepath = './vsignit/output/cheque/cheque_' + hashed_ts.hexdigest()

    newTransaction = Transaction(hashed_ts.hexdigest(), bank_userid, client_userid, st, filepath + '.png') 
    db.session.add(newTransaction)
    db.session.commit()

    return hashed_ts.hexdigest(), st, filepath

  # Function pastes the source pic on top of the destination pic
  @staticmethod
  def signcheque(client_share, client_cheque, filepath, client_username, imageFormat):
    # extract background and store as an encrypted image for colored background
    background_buffer = BytesIO()
    crop_area = (signCords[0], signCords[1], signCords[0] + \
                client_share.width, signCords[1] + client_share.height)
    cheque_bg = client_cheque.crop(crop_area)
    cheque_bg.save(background_buffer, format=imageFormat)
    encoded_bg = base64.b64encode(background_buffer.getvalue())
    Common.encryptImage(encoded_bg, filepath + '_bg.png')

    # sign cheque
    client_cheque.paste(client_share, signCords) 

    # encrypt and save the file until transaction is complete
    buffered = BytesIO()
    client_cheque.save(buffered, format=imageFormat)
    encoded_string = base64.b64encode(buffered.getvalue())
    cheque_string = base64.b64encode(buffered.getvalue())
    Common.encryptImage(cheque_string, filepath + '.png')

    # Common.save_image(client_cheque, filepath)
    # # export the image to base64 format
    # os.makedirs(os.path.dirname(filepath), exist_ok=True)
    # with open(filepath, "rb") as image_file:
    #     encoded_string = base64.b64encode(image_file.read())

    return (encoded_string.decode("utf-8") + "," + client_username)