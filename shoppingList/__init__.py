import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask.ext.sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask.ext.mail import Mail
from flask_bootstrap import Bootstrap

app = Flask(__name__)
mail = Mail(app)
Bootstrap(app)

app.config.from_object('shoppingList.config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

import shoppingList.routes