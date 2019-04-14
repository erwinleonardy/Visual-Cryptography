"""
    __init__.py
    by: Erwin Leonardy

    This file would be called automatically
    once the package 'vsignit' is called.

    It serves to initiliase the flask application
    and also the database
"""

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

UPLOAD_FOLDER = './input'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

login_manager = LoginManager()

app = Flask(__name__, template_folder='./src')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'\xdfe\x05\x86\xd1\xdc\xf6\x81\xbb\xf8\xf7_,\xba\x938'

# this code is to connect to your database
# Format: mysql://username:password@localhost/databaseName
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:erwin123@localhost/vsignit'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False    # to silent the warning message

db = SQLAlchemy(app)
login_manager.init_app(app)

from vsignit import routes
