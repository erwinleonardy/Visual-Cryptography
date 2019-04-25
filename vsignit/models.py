"""
    models.py
    by: Erwin Leonardy

    This file serves as the model (classes) 
    that is going to store the result of the
    data extracted from the database
"""
from flask_login import UserMixin
from vsignit import db, login_manager
import enum

@login_manager.user_loader
def load_user(id):
  return User.query.get(int(id))

# defines an enum for user type
class UserType(enum.Enum):
  admin = "admin"
  user = "user"

# stores user's basic information
class User(UserMixin, db.Model):
  __tablename__ = 'user_table'
  
  id = db.Column('user_id', db.Integer, primary_key=True, unique=True, nullable=False)
  user_type = db.Column(db.Enum(UserType), nullable=False)
  email = db.Column('email', db.String(100), nullable=False)
  username = db.Column('username', db.String(70), nullable=False)
  password = db.Column('password', db.String(70), nullable=False)

  def __init__ (self, username, user_type, email, password):
    self.user_type = UserType.user
    self.username = username
    self.password = password
    self.email = email

  def getUsername (self):
    return self.username

  def getID (self):
    return self.id

  def getEmail (self):
    return self.email

# stores bank's shares
class Bank_Data(UserMixin, db.Model):
  __tablename__ = 'bank_data'
  
  bank_userid = db.Column('bank_user_id', db.Integer, primary_key=True, unique=True, nullable=False)
  client_userid = db.Column('client_user_id', db.Integer, primary_key=True, unique=True, nullable=False)
  bank_share_path = db.Column('bank_share_path', db.String(100), nullable=False)

  def __init__ (self, bank_userid, client_userid, bank_share_path):
    self.bank_userid = bank_userid
    self.client_userid = client_userid
    self.bank_share_path = bank_share_path

  def getBankSharePath (self):
    return self.bank_share_path

# stores client's shares
class Client_Data(UserMixin, db.Model):
  __tablename__ = 'client_data'
  
  client_userid = db.Column('client_user_id', db.Integer, primary_key=True, unique=True, nullable=False)
  bank_userid = db.Column('bank_user_id', db.Integer, primary_key=True, unique=True, nullable=False)
  client_share_path = db.Column('client_share_path', db.String(100), nullable=False)

  def __init__ (self, client_userid, bank_userid, client_share_path):
    self.client_userid = client_userid
    self.bank_userid = bank_userid
    self.client_share_path = client_share_path

  def getBankUserId (self):
    return self.bank_userid

  def getClientSharePath (self):
    return self.client_share_path

# stores client's transaction
class Transaction(UserMixin, db.Model):
  __tablename__ = 'transaction'

  transactionNo = db.Column('transaction_number', db.String(70), primary_key=True, unique=True, nullable=False)
  bank_userid = db.Column('bank_user_id', db.Integer, nullable=False)
  client_userid = db.Column('client_user_id', db.Integer, nullable=False)
  timestamp = db.Column('timestamp', db.DateTime(), nullable=False)
  filepath = db.Column('filepath', db.String(70), nullable=False)

  def __init__ (self, transactionNo, bank_userid, client_userid, timestamp, filepath):
    self.transactionNo = transactionNo
    self.bank_userid = bank_userid
    self.client_userid = client_userid
    self.timestamp = timestamp
    self.filepath = filepath
      
  def getTranscationNo (self):
    return self.transactionNo

  def getBankId (self):
    return self.bank_userid

  def getClientId (self):
    return self.client_userid

  def getBankUsername (self):
    return User.query.filter_by(id=self.bank_userid).first().getUsername() 

  def getClientUsername (self):
    return User.query.filter_by(id=self.client_userid).first().getUsername() 

  def getTimestamp (self):
    return self.timestamp

  def getFilePath (self):
    return self.filepath 