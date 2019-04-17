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
    @staticmethod
    def register(username, password, verification):
        pw1 = hashlib.sha1()
        pw2 = hashlib.sha1()
        pw1.update(password.encode('utf-8'))
        pw2.update(verification.encode('utf-8'))
        
        if pw1.hexdigest() != pw2.hexdigest():
            return "Mismatch"

        elif (Common.userExists(username) == None):
            newUser = User(username, UserType.admin, pw1.hexdigest())
            db.session.add(newUser)
            db.session.commit()
            return "OK"

        else:
            return "DuplicatedUser"
         