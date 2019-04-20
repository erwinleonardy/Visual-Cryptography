"""
    register.py
    by: Erwin Leonardy

    This file consists of the methods
    to sign up and redirect users to the
    login page
"""

import hashlib
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
    def register(username, password, verification):
        # convert password input encoding to UTF-8
        pw1 = hashlib.sha1()
        pw2 = hashlib.sha1()
        pw1.update(password.encode('utf-8'))
        pw2.update(verification.encode('utf-8'))
        
        # if the user failed to re-enter the same password
        if pw1.hexdigest() != pw2.hexdigest():
            return "Mismatch"

        # if the password matches and the username doesn't exist
        elif (Common.userExists(username) == None):
            newUser = User(username, UserType.admin, pw1.hexdigest())
            db.session.add(newUser)
            db.session.commit()
            return "OK"

        else:
            return "DuplicatedUser"
         