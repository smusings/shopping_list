import os
from flask import Flask, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask.ext.mail import Mail
from flask_bootstrap import Bootstrap
from flask.ext.httpauth import HTTPBasicAuth

app = Flask(__name__)
mail = Mail(app)
auth = HTTPBasicAuth()
Bootstrap(app)

app.config.from_object('shoppingList.config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

@auth.get_password
def get_password(email):
    users = User.query.filter_by(email=email).first()
    if user is not None:
        return users.password
    return None

@auth.error_handler
def unauthorized():
    return jsonify({'error': 'Unauthorized access'}), 401

import shoppingList.routes