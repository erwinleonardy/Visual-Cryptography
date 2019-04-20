"""
    client.py
    by: Erwin Leonardy

    This file contains all of the necessary
    functions to operate the client page
"""

import os, time, datetime, base64, hashlib

from vsignit import db
from vsignit.common import Common, signX, signY
from vsignit.models import Transaction
from vsignit.emailerService import EmailerService

class Client:
    # adds the transaction to the database
    @staticmethod 
    def add_transaction_to_db (bank_userid, client_userid):
        clientUsername = Common.getUsernameFromID(client_userid)

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

    # sends confirmation email to client and server
    @staticmethod
    def sends_emails (transaction_no, timestamp, bank_userid, client_userid):
        clientUsername = Common.getUsernameFromID(client_userid)
        bankUsername = Common.getUsernameFromID(bank_userid)
        bank_email = Common.getUserEmail(bank_userid)
        client_email = Common.getUserEmail(client_userid)

        # send email to bank
        bankSubject = "({}) New Cheque from {}".format(bankUsername, clientUsername)
        bankMessage = """
        You have received a new cheque to be processed from {}.

        Transaction Number: {}
        Transaction Time: {}""".format(clientUsername, transaction_no, timestamp)
        EmailerService.sendEmail(bankUsername, bank_email, bankSubject, bankMessage)

        # send email to client
        clientSubject = "({}) Your cheque has been sent to {}".format(clientUsername, bankUsername)
        clientMessage = """
        Your cheque is currently being processed by {}.

        Transaction Number: {}
        Transaction Time: {}
        
        Your bank will contact you should they have any issue.""".format(bankUsername, transaction_no, timestamp)
        EmailerService.sendEmail(clientUsername, client_email, clientSubject, clientMessage)

    # paste the source pic on top of the destination pic
    @staticmethod
    def paste_on_top (source, dest, filepath, clientUsername):
        dest.paste (source,(signX, signY))   

        # save the file temporarily
        Common.save_image (dest, filepath)      

        # export the image to base64 format
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())

        return (encoded_string.decode("utf-8") + "," + clientUsername)