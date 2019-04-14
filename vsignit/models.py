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

class UserType(enum.Enum):
    admin = "admin"
    user = "user"

class User(UserMixin, db.Model):
    __tablename__ = 'user_table'
    
    id = db.Column('user_id', db.Integer, primary_key=True, unique=True, nullable=False)
    user_type = db.Column(db.Enum(UserType))
    username = db.Column('username', db.String(70), nullable=False)
    password = db.Column('password', db.String(70), nullable=False)

    def __init__ (self, username, user_type, password):
        self.user_type = UserType.user
        self.username = username
        self.password = password


# class User(db.Model):
#     __tablename__ = 'user_table'
    
#     id = db.Column('user_id', db.Integer, primary_key=True, unique=True)
#     username = db.Column('username', db.String(70))
#     password = db.Column('password', db.String(70))

#     @staticmethod
#     def getData(user):
#         return ("{}, {}, {}".format(user.id, user.username, user.password))