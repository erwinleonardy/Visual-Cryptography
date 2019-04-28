# Filename: routes.py
# Author: Erwin Leonardy
# Descrption: This file serves as the file that handles the routing of our flask program.

import base64, re, os, time, requests
from flask import render_template, request, url_for, redirect, session, jsonify
from flask_login import current_user, logout_user
from PIL import Image
from datetime import timedelta

from vsignit import app
from vsignit.driver import Driver
from vsignit.common import Common
from vsignit.models import UserType, User, Client_Data, Transaction

@app.route('/', methods=['GET'])
def index():
  if not current_user.is_authenticated:
    username = ""
    authenticated = "False"
    user_type = ""
    
  else:
    result = User.query.filter_by(id=current_user.get_id()).first()
    username = result.getUsername()
    authenticated = "True"

    if result.user_type == UserType.admin:
      user_type = "Bank"
    else:
      user_type = "Client"

  return render_template('learning-tool.html', authenticated=authenticated, username=username, user_type = user_type)
  
  # if not current_user.is_authenticated:
  #   return redirect(url_for('login'))
  # else:
  #     # get user type
  #     usertype = User.query.filter_by(id=current_user.get_id()).first().user_type

  #     # redirect page based on user type
  #     if usertype == UserType.admin:
  #       return redirect(url_for('bank_generate'))
  #     elif usertype == UserType.user:
  #       return redirect(url_for('client'))
  #     else:
  #       return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'GET':
    if not current_user.is_authenticated:
      try:
        return render_template('login.html', authenticated="False")
      except Exception as e:
        return str(e)
    else:
      return redirect(url_for('index'))

  elif request.method == 'POST':  
    username = request.form['username']
    password = request.form['password']

    return Driver.login(username, password)

@app.route('/register', methods=['GET', 'POST'])
def register():
  if request.method == 'GET':
      if not current_user.is_authenticated:
        try:
          return render_template('register.html', authenticated="False")
        except Exception as e:
          return str(e)
      else:
        return redirect(url_for('index'))

  elif request.method == 'POST':  
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    verification = request.form['verification']

    return Driver.register (username, email, password, verification)

@app.route('/logout')
def logout():
  logout_user()
  return redirect(url_for('index'))

@app.route('/bank-generate', methods=['GET', 'POST'])
def bank_generate():
  if request.method == 'GET':
      try:
        # checks if user is logged in
        result = User.query.filter_by(id=current_user.get_id()).first()

        # redirects page according to the result
        if not current_user.is_authenticated or result == None:
          logout_user()
          return redirect(url_for('login'))

        else:
          return render_template('bank-generation.html', result=result)

      except Exception as e:
        return str(e)

  elif request.method == 'POST':      
    # convert the base64 image to an image
    base64_data = re.sub('^data:image/.+;base64,', '', request.form['file'])
    byte_data = base64.b64decode(base64_data)

    username = request.form['clientUsername']
    filepath = "./vsignit/output/tmp/" + username + "_imageToSave.png"

    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "wb") as fh:
      fh.write(byte_data)

    # generate two shares and send one of the shares to the server
    image = Common.open_image (filepath, 1)

    # checks if the image dimension is valid
    if Common.validate_resize_image(image) != None:
      bank_share = Driver.create_shares(image, username)
      os.remove("./vsignit/output/tmp/" + username + "_imageToSave.png")
      return bank_share

    else:
      return ""

@app.route('/bank-reconstruct', methods=['GET', 'POST'])
def bank_reconstruct():
  if request.method == 'GET':
    try:
      # checks if user is logged in
      result = User.query.filter_by(id=current_user.get_id()).first()

      # redirects page according to the result
      if not current_user.is_authenticated or result == None:
        logout_user()
        return redirect(url_for('login'))
      
      else:
        # extracts the pending cheques of that particular bank
        transactions = Common.get_bank_transactions(current_user.get_id())

        return render_template('bank-reconstruct.html', result=result, transactions=transactions)
    except Exception as e:
      return str(e)

  elif request.method == 'POST':  
    # retrieve the transaction from the DB
    transactionNo = request.form['transactionNo']
    transaction = Transaction.query.filter_by(transactionNo=transactionNo).first()

    # reconsruct the share and return base64 encoding to the admin
    if request.form['type'] == 'Verify':
      return "/bank-reconstruct/verify?transID=" + transactionNo

    # if admin chooses to delete a transaction
    elif request.form['type'] == 'Delete':
      Driver.transaction_deletion (transaction)

    return ""

@app.route('/bank-reconstruct/verify', methods=['GET', 'POST'])
def bank_reconstruct_verify():
  if request.method == 'GET':
    try:
      # checks if user is logged in
      result = User.query.filter_by(id=current_user.get_id()).first()

      # redirects page according to the result
      if not current_user.is_authenticated or result == None:
        logout_user()
        return redirect(url_for('login'))
    
      else:
        # extracts the transaction
        transactionNo = request.args.get('transID')
        transaction = Transaction.query.filter_by(transactionNo=transactionNo).first()

        # reconstruct the share and sends the base64 to the client
        recon_cheque, clean1, recon = Driver.reconstruct_shares (transaction)

        return render_template('verify.html', result=result, transaction=transaction, recon_cheque=recon_cheque, clean1=clean1, recon=recon)
    except Exception as e:
        return str(e)

  elif request.method == 'POST':  
    # retrieve the transaction from the DB
    transactionNo = request.form['transactionNo']
    transaction = Transaction.query.filter_by(transactionNo=transactionNo).first()

    # verify the given cheque
    Driver.transaction_verification(transaction, request.form['response'])

    # delete the transaction
    Driver.transaction_deletion (transaction)
        
    return url_for('bank_reconstruct')
            
    
@app.route('/client', methods=['GET', 'POST'])
def client():
  if request.method == 'GET':
    try:
      # checks if user is logged in
      result = User.query.filter_by(id=current_user.get_id()).first()

      # redirects page according to the result
      if not current_user.is_authenticated or result == None:
          logout_user()
          return redirect(url_for('login'))

      else:
        # extracts the bank the client subscribed to
        usernames = Common.get_bank_usernames(current_user.get_id())

        return render_template('client.html', result=result, usernames=usernames, clientName=result.getUsername())
    except Exception as e:
        return str(e)

  elif request.method == 'POST':
    # retrieve the client's share from the databse
    clientUsername = User.query.filter_by(id=current_user.get_id()).first().getUsername()
    bankUsername = request.form['bankName']

    clientID = current_user.get_id()
    bankID = User.query.filter_by(username=bankUsername).first().getID()

    clientSharePath = Client_Data.query.filter_by(client_userid=clientID, bank_userid=bankID).first().getClientSharePath()

    # convert the base64 image to an image
    base64_data1 = re.sub('^data:image/.+;base64,', '', request.form['cheque'])
    byte_data1 = base64.b64decode(base64_data1)
    filepath = "./vsignit/output/tmp/" + clientUsername + "_clientCheque.png"

    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "wb") as fh:
      fh.write(byte_data1)

    # get the clientCheque and clientShare that we are going to overlay
    clientCheque = Common.open_image (filepath, 1)
    clientShare = Common.open_image (clientSharePath, 1)

    # paste the client share on top of the blank share given by the client
    resultStr = Driver.client_signcheque (clientShare, clientCheque, clientID, bankID)

    # remove the temporary clientcheque file
    os.remove(filepath)

    return resultStr

# print(request.form['file1'], file=sys.stderr)