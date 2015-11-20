import os

DEBUG = True
SECRET_KEY = 'github'
SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.dirname(os.path.realpath(__file__))+'/db/eugenet.db'