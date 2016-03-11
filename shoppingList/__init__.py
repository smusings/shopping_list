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

import shoppingList.routes