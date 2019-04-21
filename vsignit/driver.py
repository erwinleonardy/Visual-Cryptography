"""
    driver.py
    by: Erwin Leonardy

    This file contains all of the necessary
    functions to run the web application.
"""

from __future__ import print_function
from PIL import Image
from flask_login import login_user
from flask import url_for
import PIL.ImageOps
import re, time, base64, sys, os

from vsignit.shareSplitter import ShareSplitter
from vsignit.shareReconstructor import ShareReconstuctor
from vsignit.common import Common
from vsignit.login import Login
from vsignit.register import Register
from vsignit.client import Client

"""
Functions
"""
class Driver():
    """
        Login to the system
    """
    @staticmethod
    def login (username, password):
        result = Login.login(username, password)  

        if result != None:
            login_user(result)
            return url_for('index')
            
        else:
            return ""

    """
        Register the user to the system
    """
    @staticmethod
    def register (username, email, password, verification):
        return Register.register(username, email, password, verification)

    """
        Share Splitter Driver Function
    """
    @staticmethod
    def share_splitter (image, username):
        # checks if the username exists
        if Common.userExists(username) == None:
            return "No User"

        # resize the image
        image = ShareSplitter.resize(image)

        # split into two shares
        outfile1, outfile2 = ShareSplitter.split_signature (image)

        # send the shares to the 
        encoded_str = ShareSplitter.send_shares (outfile1, outfile2, username)

        return encoded_str

    """
        Share Reconstruction Driver Function
    """
    @staticmethod
    def share_reconstruction (transaction):
        # retrieves the client cheque
        transactionNo, clientUsername, clientCheque = ShareReconstuctor.getClientCheque (transaction)

        # retrieves the bankShare
        bankShare = ShareReconstuctor.getBankShare (transaction)
        
        # reconstruct the shares based on the client cheque and bank share given
        outfile = ShareReconstuctor.reconstruct_shares(transactionNo, clientCheque, bankShare)
        
        # if error occurs, it will return None
        if outfile == None:
            return ""

        # else, proceed
        else:
            # pass through 2 cleaning processes
            outfile = ShareReconstuctor.remove_noise(transactionNo, outfile)

            # send the reconstructed shares to the client
            encoded_str = ShareReconstuctor.send_reconstructed(transactionNo, clientUsername, clientCheque, outfile)

            return encoded_str

    """
        Delete the transaction from the DB
    """
    @staticmethod
    def transaction_deletion (transaction):
        # delete existing image
        ShareReconstuctor.delete_cheque (transaction)

        # delete the share from the DB and remove the image
        ShareReconstuctor.delete_transaction (transaction)

        print ("Deletion!!!!\n\n\n\n")

    """
        Client Page Driver Function
    """
    @staticmethod
    def overlay_cheque (clientShare, clientCheque, client_userid, bank_userid):
        # get the client's username based on the id
        clientUsername = Common.getUsernameFromID(client_userid)

        # adds this current transcation to the databsase
        transactionNo, timestamp, filepath = Client.add_transaction_to_db (bank_userid, client_userid)

        # sends an email notification to both bank and client
        Client.sends_emails(transactionNo, timestamp, bank_userid, client_userid)

        # overlays the client share on top of the cheque
        result = Client.paste_on_top (clientShare, clientCheque, filepath, clientUsername)

        return result
        