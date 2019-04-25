# Filename: __init__.py
# Author: Erwin Leonardy
# Descrption: This file would be called automatically once the package 'vsignit' is called.
#             It serves to initiliase the flask application and also the database

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

# basic configuration
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__, template_folder='./src')
app.config.from_pyfile('flask.cfg')

# initialise the SQLAlchemy database and Mail
db = SQLAlchemy(app)
mail = Mail(app)

# initialize login_manager
login_manager = LoginManager()
login_manager.init_app(app)

# routes is only imported here because it needs the access
# to the 'app' object
from vsignit import routes
