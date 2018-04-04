import os
import sys
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_bootstrap import Bootstrap
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()
Bootstrap(app)

app.config.from_object('shoppingList.config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

def not_implimented():
    resp = jsonify(message = {
            'status': 501,
            'message': 'Not Implimented',
        }), 501
    return resp

import shoppingList.routes.routes