"""
    shareReconstructor.py
    by: Erwin Leonardy

    This file contains all of the necessary
    functions to reconstruct the shares
"""

from PIL import Image
import PIL.ImageOps
import base64, os

from vsignit.common import Common
from vsignit.common import signX, signY, signWidth, doubSignSize, reconDist

class ShareReconstuctor():
    """
        This function reconstructs the image 
        using two of the shares
    """
    @staticmethod
    def reconstruct_shares (clientCheque, bankShare):
        bankWidth, bankHeight = bankShare.size
        signWidth = int(bankWidth / 2)
        doubSignSize = signWidth * 2

        # extract the shares area
        clientShare = clientCheque.crop((signX, signY, signX+(doubSignSize), signY+(doubSignSize)))
        clientShare.thumbnail((doubSignSize, doubSignSize), Image.ANTIALIAS)
        clientShare = clientShare.convert('1')
        clientWidth, clientHeight = clientShare.size

        print("clientWidth: {}, clientHeight: {}".format(clientWidth, clientHeight))
        print("bankWidth: {}, bankHeight: {}".format(bankWidth, bankHeight))

        if (bankWidth == clientWidth and bankHeight == clientHeight): 
            try:
                # reconstruct the shares
                outfile = Image.new('1', clientShare.size)

                for x in range(clientShare.size[0]):
                    for y in range(clientShare.size[1]): 
                        outfile.putpixel((x,y), min(clientShare.getpixel((x, y)), bankShare.getpixel((x, y))))

                Common.save_image (outfile, "recon")    

                return outfile
            
            except IndexError:
                return ""

        else:
            return ""

    """
        This function resizes the reconstructed 
        image and clean the noise
    """
    @staticmethod
    def remove_noise (inputImg):
        outfile = Image.new("1", [int(dimension / 2) for dimension in inputImg.size], 255)
        length, width = inputImg.size

        # Cleaning (Phase 1)
        # only writes black iff
        # the (2x2) block is black
        # i.e.
        # B B
        # B B
        for yIn, yOut in zip(range(0,width,2), range(width)):
            for xIn, xOut in zip(range(0,length,2), range(length)):
                if (inputImg.getpixel((xIn, yIn)) != 255 and
                    inputImg.getpixel((xIn + 1, yIn)) != 255 and
                    inputImg.getpixel((xIn, yIn + 1)) != 255 and
                    inputImg.getpixel((xIn + 1, yIn + 1)) != 255):
                    outfile.putpixel((xOut, yOut), 0)

        Common.save_image (outfile, "clean1")
    
        # Cleaning (Phase 2)
        # only writes black iff
        # the block has following pattern
        # i.e.
        # W B  =>  W W
        # B B      W W
        result = outfile
        for y in range (0,result.size[0], 2):
            for x in range (0, result.size[1], 2):
                if (outfile.getpixel((x,y)) == 255 and
                    outfile.getpixel((x + 1, y)) == 0 and
                    outfile.getpixel((x, y + 1)) == 0 and
                    outfile.getpixel((x + 1, y + 1)) == 0):
                    result.putpixel((x + 1, y), 255)
                    result.putpixel((x, y + 1), 255)
                    result.putpixel((x + 1, y + 1), 255)
        
        # create transparent layer to be pasted on cheque
        image_trans = Image.new("RGBA", (result.size[0], result.size[1]), (255,255,255,0))

        for y in range (0,result.size[0]):
            for x in range (0, result.size[1]):
                if (outfile.getpixel((x,y)) == 0):
                    image_trans.putpixel((x,y), (0,0,0,255))

        Common.save_image (image_trans, "clean2")

        return outfile

    """
        This function will allow the bank's share 
        to be downloaded
    """
    @staticmethod
    def send_reconstructed (username, clientCheque, outfile):
        # replace the area with white color
        for x in range(signX, signX+(doubSignSize)):
            for y in range(signY, signY+(doubSignSize)):
                clientCheque.putpixel((x, y), 255)

        # place the clean shares to it
        Common.overlay_pic("./vsignit/output/clean2.png", clientCheque)

        # send back the final cheque to the bank using AJAX
        with open("./vsignit/output/final_cheque.png", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())

        os.remove("./vsignit/output/final_cheque.png")

        return (encoded_string.decode("utf-8") + "," + username)