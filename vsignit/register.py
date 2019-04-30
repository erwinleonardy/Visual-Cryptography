# Filename: register.py
# Author: Erwin Leonardy
# Descrption: This file consists of the methods to sign up and redirect users to the login page

from werkzeug.security import generate_password_hash

from vsignit.models import UserType, User
from vsignit.common import Common
from vsignit import db

class Register():
  # Function registers the users if and only if the username
  # doesn't exist and both of the password match
  @staticmethod
  def register(username, email, password, verification):
    # if the user failed to re-enter the same password
    # else if the password matches and the username doesn't exist
    if password != verification:
      return "Both of the password doesn't match!"
    elif (Common.email_exists(email) != None):
      return "This email has been used to register a vSignIt account before!"
    elif (Common.user_exists(username) == None):
      newUser = User(username, UserType.admin, email, generate_password_hash(password))
      db.session.add(newUser)
      db.session.commit()
      return "/login"
    else:
      return "The username '" + username + "' already exists!"