import os
from flask import Flask, render_template, request, redirect, url_for, session
from models import db, User, List, Item

app = Flask(__name__)

app.config.from_object('shoppingList.config')

import shoppingList.routes