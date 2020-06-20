import os
from os import environ

basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = environ.get('SECRET_KEY')

JWT_SECRET = environ.get('JWT_SECRET')

SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'kisaw.db')
SQLALCHEMY_ECHO=True
SQLALCHEMY_TRACK_MODIFICATIONS = False
