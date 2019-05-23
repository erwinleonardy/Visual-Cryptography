# Filename: register.py
# Author: Erwin Leonardy
# Descrption: This file consists of the methods to sign up and redirect users to the login page

import re
from werkzeug.security import generate_password_hash

from vsignit.models import UserType, User
from vsignit.common import Common
from vsignit import db

class Register():
  def __init__(self, username, email, password, verification):
    self.username = username
    self.email = email
    self.password = password
    self.verification = verification

  # Function registers the users if and only if the username
  # doesn't exist and both of the password match
  def register(self):
    # Verify the strength of 'password'
    # A password is considered strong if:
    #     8 characters length or more
    #     1 digit or more
    #     1 symbol or more
    #     1 uppercase letter or more
    #     1 lowercase letter or more

    # calculating the length
    if len(self.password) < 8:
      return "Your password should have at least 8 characters!"

    # searching for digits
    elif re.search(r"\d", self.password) is None:
      return "Your password should have at least a digit or more!"

    # searching for uppercase
    elif re.search(r"[A-Z]", self.password) is None:
      return "Your password should have at least one uppercase letter!"

    # searching for lowercase
    elif re.search(r"[a-z]", self.password) is None:
      return "Your password should have at least one lowercase letter!"

    # searching for symbols
    elif re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~"+r'"]', self.password) is None:
      return "Your password should have at least one symbol!"

    # if the user failed to re-enter the same password
    # else if the password matches and the username doesn't exist
    if self.password != self.verification:
      return "Both of the password doesn't match!"
    elif (Common.email_exists(self.email) != None):
      return "This email has been used to register a vSignIt account before!"
    elif (Common.user_exists(self.username) == None):
      newUser = User(self.username, UserType.admin, self.email, generate_password_hash(self.password))
      db.session.add(newUser)
      db.session.commit()
      return "/login"
    else:
      return "The username '" + self.username + "' already exists!"