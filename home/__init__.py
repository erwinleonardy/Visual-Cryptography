from flask import Flask

home = Flask(__name__)

from home import routes

print (__name__)