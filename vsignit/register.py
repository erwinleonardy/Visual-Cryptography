"""
    register.py
    by: Erwin Leonardy

    This file consists of the methods
    to sign up and redirect users to the
    login page
"""

from werkzeug.security import generate_password_hash
from vsignit import db
from vsignit.models import UserType, User
from vsignit.common import Common

class Register():
  """
      This function only registers the users if
      and only if the username doesn't exist and
      both of the password match
  """
  @staticmethod
  def register(username, email, password, verification):
    # if the user failed to re-enter the same password
    if password != verification:
      return "Both of the password doesn't match!"

    # if the password matches and the username doesn't exist
    elif (Common.userExists(username) == None):
      newUser = User(username, UserType.admin, email, generate_password_hash(password))
      db.session.add(newUser)
      db.session.commit()
      return "/login"

    else:
      return "The username '" + username + "' already exists!"
      