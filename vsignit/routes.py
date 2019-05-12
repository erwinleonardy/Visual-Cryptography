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
  # if not current_user.is_authenticated:
  #   username = ""
  #   authenticated = "False"
  #   user_type = ""
    
  # else:    
  
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

@app.route('/learning', methods=['GET', 'POST'])
def learning():
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
    sigEncoded = re.sub('^data:image/.+;base64,', '', request.form['file'])
    username = request.form['clientUsername']

    shareStatus = Driver.create_shares(sigEncoded, username)
    return shareStatus


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
      # if cheque can't be deleted
      try:
        Driver.transaction_deletion (transaction)
      except ValueError:
        return "/bank-reconstruct/verify"

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

        try:
          # if user enters without entering transactionID
          if transactionNo == None:
            raise ValueError
            
          else:
            # reconstruct the share and sends the base64 to the client
            recon_cheque, clean1, recon = Driver.reconstruct_shares (transaction)
            return render_template('verify.html', result=result, transaction=transaction, recon_cheque=recon_cheque, clean1=clean1, recon=recon)
        
        # if there is something wrong
        except ValueError:
          return render_template('verify.html', result=None)
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
    bankID = User.query.filter_by(username=request.form['bankName']).first().getID()
    clientID = current_user.get_id()

    chequeEncoded = re.sub('^data:image/.+;base64,', '', request.form['cheque'])
    clientSharePath = Client_Data.query.filter_by(client_userid=clientID, bank_userid=bankID).first().getClientSharePath()

    # paste the client share on top of the blank share given by the client
    signStatus = Driver.client_signcheque (clientID, bankID, chequeEncoded, clientSharePath)
    return signStatus
