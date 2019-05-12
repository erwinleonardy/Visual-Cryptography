# Filename: login.py
# Author: Erwin Leonardy
# Descrption: This file consists of the methods to login and redirect users to the intended page

from werkzeug.security import check_password_hash
from flask_login import login_user

from vsignit.models import User

class Login():
  def __init__(self, username, password):
    self.username = username
    self.password = password

  # Function Checks if the username and password provided can be found in the databse
  def login(self):
    login = False
    user = User.query.filter_by(username= self.username).first()
    if user is not None and check_password_hash(user.password,  self.password):
      login_user(user)
      login = True
    
    return login