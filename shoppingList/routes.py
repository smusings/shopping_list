import math
import requests
from shoppingList import app, db, auth, not_implimented
from flask import render_template, request, redirect, url_for, session, jsonify
from shoppingList.models import User, List, Item, UserList
from shoppingList.item import item_json, delete_item_json, json_list
from shoppingList.list import get_list, delete_table_json, shopping_list

# Auth
@auth.get_password
def get_password(email):
    users = User.query.filter_by(email=email).first()
    if users is not None:
        return users.password
    return None

@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username).first()
    if not user:
        return False
    return user.check_password(password)

@auth.error_handler
def unauthorized():
    return jsonify({'error': 'Unauthorized access'}), 401

# Routes
@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        lst = []
        if session.get('user'):
            user = session.get('user')
            lst = UserList.query.filter(UserList.user_id == user).all()
        return render_template('shopping_lists.html', lists = lst)

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/createList')
def create_list():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('new_list.html')

@app.route('/list/<int:id>')
def view_list(id):
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('list.html', list_id = id)

@app.route('/login', methods=['POST'])
def login():
    user = User.query.filter_by(email=request.form['username']).first()
    error = None
    if request.method == 'POST':
        if user is None:
            error = 'Invalid Email'
        else:
            if not user.check_password(request.form['password']):
                error = 'Invalid Password'
            else:
                session['logged_in'] = True
                session['user'] = user.id
                return redirect(url_for('home'))
        print error
        return render_template('login.html', error = error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user', None)
    return redirect(url_for('home'))