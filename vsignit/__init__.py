# Filename: __init__.py
# Author: Erwin Leonardy
# Descrption: This file would be called automatically once the package 'vsignit' is called.
#             It serves to initiliase the flask application and also the database

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask import Flask

import os, firebase_admin
from firebase_admin import credentials
from google.cloud import storage

app = Flask(__name__, template_folder='./src')
app.config.from_pyfile('flask.cfg')

# initialise the database, mail, login_manager
db = SQLAlchemy(app)
mail = Mail(app)

# initialize login_manager
login_manager = LoginManager()
login_manager.init_app(app)

# connect to Google Firebase and get the default 'bucket'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './vsignit/vsignit-app-firebase-adminsdk-eo7f1-ad2b3acabb.json'
cred = credentials.Certificate("./vsignit/vsignit-app-firebase-adminsdk-eo7f1-ad2b3acabb.json")
default_firestore = firebase_admin.initialize_app(cred, {
    'storageBucket':'gs://vsignit-app.appspot.com'
})
client = storage.Client()
bucket = client.get_bucket('vsignit-app.appspot.com')

# routes is only imported here because it needs access
# to the 'app' object
from vsignit import routes
