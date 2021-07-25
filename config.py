import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

SQLALCHEMY_TRACK_MODIFICATIONS = False

# Connect to the database
database_filename = "database.db"
SQLALCHEMY_DATABASE_URI = "sqlite:///{}".format(os.path.join(basedir, database_filename))

app = Flask(__name__)

app.config.from_object('config')
db = SQLAlchemy(app)
