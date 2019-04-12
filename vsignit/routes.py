"""
    routes.py
    by: Erwin Leonardy

    This file serves as the file that
    handles the routing of our flask program.
"""

import base64, re, os
from flask import render_template, request, session, url_for, redirect
from flask_login import current_user, login_user, logout_user

from vsignit import app
from vsignit.login import Login
from vsignit.driver import Driver
from vsignit.common import Common
from vsignit.models import UserType, User

@app.route('/', methods=['GET'])
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    else:
        # get user type
        usertype = User.query.filter_by(id=current_user.get_id()).first().user_type

        # redirect page based on user type
        if usertype == UserType.admin:
            return redirect(url_for('bank_generate'))
        elif usertype == UserType.user:
            return redirect(url_for('client'))
        else:
            return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if not current_user.is_authenticated:
            try:
                return render_template('login.html')
            except Exception as e:
                return str(e)
        else:
            return redirect(url_for('index'))

    elif request.method == 'POST':  
        username = request.form['username']
        password = request.form['password']

        result = Login.login(username, password)  

        if result != None:
            login_user(result)
            return url_for('index')
            
        else:
            return ""

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/forbidden')
def forbidden():
    return render_template('forbidden.html')

@app.route('/bank-generate', methods=['GET', 'POST'])
def bank_generate():
    if request.method == 'GET':
        try:
            result = User.query.filter_by(id=current_user.get_id()).first()

            if not current_user.is_authenticated or result == None:
                logout_user()
                return redirect(url_for('login'))

            else:
                if result.user_type != UserType.admin:
                    return redirect(url_for('forbidden'))
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
        image = Common.open_image ("imageToSave.png", 1)

        # checks if the image dimension is valid
        if Common.validate_resize_image(image) != None:
            username = request.form['filename'].split(".")[0]
            email = request.form['email']

            bank_share = Driver.share_splitter(email, image, username)

            os.remove("./vsignit/input/imageToSave.png")
            return bank_share

        else:
            return ""

@app.route('/bank-reconstruct', methods=['GET', 'POST'])
def bank_reconstruct():
    if request.method == 'GET':
        try:
            result = User.query.filter_by(id=current_user.get_id()).first()

            if not current_user.is_authenticated or result == None:
                logout_user()
                return redirect(url_for('login'))
            
            else:
                if result.user_type != UserType.admin:
                    return redirect(url_for('forbidden'))
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
        clientCheque = Common.open_image ("clientCheque.png", 1)
        bankShare = Common.open_image ("bankShare.png", 1)

        final_result = Driver.share_reconstruction (clientCheque, bankShare, username)
        # final_result = Driver.share_reconstruction (clientCheque, bankShare, username)

        os.remove("./vsignit/input/clientCheque.png")
        os.remove("./vsignit/input/bankShare.png")

        return final_result
    
@app.route('/client', methods=['GET', 'POST'])
def client():
    if request.method == 'GET':
        try:
            result = User.query.filter_by(id=current_user.get_id()).first()

            if not current_user.is_authenticated or result == None:
                logout_user()
                return redirect(url_for('login'))

            else:
                if result.user_type != UserType.user:
                    return redirect(url_for('forbidden'))
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
        clientCheque = Common.open_image ("clientCheque.png", 1)
        clientShare = Common.open_image ("clientShare.png", 1)

        resultStr = Common.paste_on_top (clientShare, clientCheque, username)

        os.remove("./vsignit/input/clientCheque.png")
        os.remove("./vsignit/input/clientShare.png")

        return resultStr