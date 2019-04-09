"""
    models.py
    by: Erwin Leonardy

    This file serves as the model (classes) 
    that is going to store the result of the
    data extracted from the database
"""

from vsignit import db

class User(db.Model):
    __tablename__ = 'user_table'
    
    id = db.Column('user_id', db.Integer, primary_key=True, unique=True)
    username = db.Column('username', db.String(70))
    password = db.Column('password', db.String(70))

    @staticmethod
    def getData(user):
        return ("{}, {}, {}".format(user.id, user.username, user.password))

# class User(db.Model):
#     __tablename__ = 'user_table'
#     id = db.Column('user_id', db.Integer, primary_key=True, unique=True)
#     username = db.Column('username', db.String(70))
#     password = db.Column('password', db.String(70))
  
#     def getData(self):
#         data = self.query.all()[0]
#         print("Created!!")
#         print("\n\n\n\n\n")
#         print("Test!!")
#         print("Called!!")
#         print ("{}, {}, {}".format(data.id, data.username, data.password))
