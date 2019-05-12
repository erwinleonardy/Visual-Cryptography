# Filename: register.py
# Author: Erwin Leonardy
# Descrption: This file consists of the methods to sign up and redirect users to the login page

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