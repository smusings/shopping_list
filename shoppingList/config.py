import os
from datetime import timedelta

DEBUG = True
SECRET_KEY = 'github'
PERMANENT_SESSION_LIFETIME = timedelta(minutes=20)
SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.dirname(os.path.realpath(__file__))+'/db/eugenet.db'