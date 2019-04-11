"""
    login.py
    by: Erwin Leonardy

    This file consists of the methods
    to login and redirect users to the
    intended page
"""

import hashlib
from vsignit.models import User

class Login():
    @staticmethod
    def login(username, password):
        sha_1 = hashlib.sha1()
        sha_1.update(password.encode('utf-8'))
        return User.query.filter_by(username=username, password=sha_1.hexdigest()).first()