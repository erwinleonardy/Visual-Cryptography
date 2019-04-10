"""
    driver.py
    by: Erwin Leonardy

    This file contains all of the necessary
    functions to run the web application.
"""

from __future__ import print_function
from PIL import Image
import PIL.ImageOps
import re, time, base64, sys, os

from vsignit.shareSplitter import ShareSplitter
from vsignit.shareReconstructor import ShareReconstuctor
from vsignit.common import Common

"""
Functions
"""
class Driver():
    """
        Share Splitter Driver Function
    """
    @staticmethod
    def share_splitter (email, image, username):
        # resize the image
        image = ShareSplitter.resize(image)

        # split into two shares
        outfile1, outfile2 = ShareSplitter.split_signature (image)

        # send the shares to the 
        encoded_str = ShareSplitter.send_shares (outfile1, outfile2, email, username)

        return encoded_str

    """
        Share Reconstruction Driver Function
    """
    @staticmethod
    def share_reconstruction (clientCheque, bankShare, username):
        # attempt to reconstruct the share
        outfile = ShareReconstuctor.reconstruct_shares(clientCheque, bankShare)
        
        # if error occurs, it will return None
        if outfile == None:
            return ""

        # else, proceed
        else:
            # pass through 2 cleaning processes
            outfile = ShareReconstuctor.remove_noise(outfile)

            # send the reconstructed shares to the client
            encoded_str = ShareReconstuctor.send_reconstructed(username, clientCheque, outfile)

            return encoded_str

    """
        Share Reconstruction Driver Function
    """
    @staticmethod
    def drop_share (source, dest, username):
        Common.paste_on_top (source, dest, username)