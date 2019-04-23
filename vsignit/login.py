"""
    login.py
    by: Erwin Leonardy

    This file consists of the methods
    to login and redirect users to the
    intended page
"""

from werkzeug.security import check_password_hash
from flask_login import login_user
from vsignit.models import User

class Login():
  """
      Checks if the username and password
      provided can be found in the databse
  """
  @staticmethod
  def login(username, password):
    login = False
    user = User.query.filter_by(username=username).first()
    if user is not None and check_password_hash(user.password, password):
      login_user(user)
      login = True
    
    return login