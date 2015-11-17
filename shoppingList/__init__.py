import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object('shoppingList.config')

db = SQLAlchemy(app)

import shoppingList.routes