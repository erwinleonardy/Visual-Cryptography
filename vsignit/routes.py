"""
    routes.py
    by: Erwin Leonardy

    This file serves as the file that
    handles the routing of our flask program.
"""

import base64, re, os
from flask import render_template, request

from vsignit import app
from vsignit.driver import Driver
from vsignit.models import User

@app.route('/')
def default_client():
    try:
        user = User.query.all()
        print(User.getData(user[0]))

        return render_template('admin-generation.html')
    except Exception as e:
        return str(e)

@app.route('/bank-generate', methods=['GET', 'POST'])
def bank_generate():
    if request.method == 'GET':
        try:
            return render_template('admin-generation.html')
        except Exception as e:
            return str(e)

    elif request.method == 'POST':        
        # print(request.form['file'], file=sys.stderr)

        # convert the base64 image to an image
        base64_data = re.sub('^data:image/.+;base64,', '', request.form['file'])
        byte_data = base64.b64decode(base64_data)

        with open("./vsignit/input/imageToSave.png", "wb") as fh:
            fh.write(byte_data)

        # generate two shares and send one of the shares to the server
        image = Driver.open_image ("imageToSave.png", 1)

        if Driver.validate_resize_image(image) != None:
            username = request.form['filename'].split(".")[0]
            email = request.form['email']
            bank_share = Driver.gen_2shares(email, image, username)

            os.remove("./vsignit/input/imageToSave.png")
            return bank_share

        else:
            return ""

@app.route('/bank-reconstruct', methods=['GET', 'POST'])
def bank_reconstruct():
    if request.method == 'GET':
        try:
            return render_template('admin-reconstruct.html')
        except Exception as e:
            return str(e)

    elif request.method == 'POST':        
        # print(request.form['file1'], file=sys.stderr)

        username = request.form['filename'].split("_")[0]

        # convert the base64 image to an image
        base64_data1 = re.sub('^data:image/.+;base64,', '', request.form['file1'])
        byte_data1 = base64.b64decode(base64_data1)

        base64_data2 = re.sub('^data:image/.+;base64,', '', request.form['file2'])
        byte_data2 = base64.b64decode(base64_data2)

        with open("./vsignit/input/clientCheque.png", "wb") as fh:
            fh.write(byte_data1)

        with open("./vsignit/input/bankShare.png", "wb") as fh:
            fh.write(byte_data2)

        # merge the client cheque and the bank share
        # to reveal the reconstructed signature
        clientCheque = Driver.open_image ("clientCheque.png", 1)
        bankShare = Driver.open_image ("bankShare.png", 1)

        final_result = Driver.merge_2shares (clientCheque, bankShare, username)

        os.remove("./vsignit/input/clientCheque.png")
        os.remove("./vsignit/input/bankShare.png")

        return final_result
    
@app.route('/client', methods=['GET', 'POST'])
def client():
    if request.method == 'GET':
        try:
            return render_template('client.html')
        except Exception as e:
            return str(e)

    elif request.method == 'POST':
        # print(request.form['file1'], file=sys.stderr)

        username = request.form['filename'].split("_")[0]

        if ".png" in username or ".jpg" in username:
            return ""

        # convert the base64 image to an image
        base64_data1 = re.sub('^data:image/.+;base64,', '', request.form['file1'])
        byte_data1 = base64.b64decode(base64_data1)

        base64_data2 = re.sub('^data:image/.+;base64,', '', request.form['file2'])
        byte_data2 = base64.b64decode(base64_data2)

        with open("./vsignit/input/clientCheque.png", "wb") as fh:
            fh.write(byte_data1)

        with open("./vsignit/input/clientShare.png", "wb") as fh:
            fh.write(byte_data2)

        # generate two shares and send one of the shares to the server
        clientCheque = Driver.open_image ("clientCheque.png", 1)
        clientShare = Driver.open_image ("clientShare.png", 1)

        resultStr = Driver.paste_on_top (clientShare, clientCheque, username)

        os.remove("./vsignit/input/clientCheque.png")
        os.remove("./vsignit/input/clientShare.png")

        return resultStr