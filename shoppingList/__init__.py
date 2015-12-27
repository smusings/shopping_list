import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.mail import Mail

app = Flask(__name__)
mail = Mail(app)

app.config.from_object('shoppingList.config')

db = SQLAlchemy(app)

import shoppingList.routes