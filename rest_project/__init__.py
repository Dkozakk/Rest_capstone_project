from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from configparser import ConfigParser

import os


parser = ConfigParser()


parser.read('config.ini')

database = parser['database']

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =  database['Database_uri']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = bool(database['Track_modifications'])
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', '12345678b9a0a9b87654321')

db = SQLAlchemy(app)
