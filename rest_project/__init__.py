import os
from configparser import ConfigParser

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

parser = ConfigParser()

file_dir = os.path.dirname(__file__)
config = os.path.join(file_dir, 'configs', 'config.ini')
parser.read(config)

database = parser['database']

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = database.get('database_uri')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = database.getboolean('track_modifications')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', '12345678b9a0a9b87654321')

db = SQLAlchemy(app)
