"""
    __init__.py
    by: Erwin Leonardy

    This file would be called automatically
    once the package 'vsignit' is called.

    It serves to initiliase the flask application
    and also the database
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

UPLOAD_FOLDER = './input'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


app = Flask(__name__, template_folder='./src')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# this code is to connect to your database
# Format: mysql://username:password@localhost/databaseName
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:erwin123@localhost/vsignit'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False    # to silent the warning message
db = SQLAlchemy(app)

from vsignit import routes
