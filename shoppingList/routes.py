import math
import requests
from shoppingList import app, db, auth
from flask import render_template, request, redirect, url_for, session, jsonify
from shoppingList.models import User, List, Item, UserList
from shoppingList.item import item_json, delete_item_json, json_list
from shoppingList.list import get_list, delete_table_json, shopping_list
from requests.auth import HTTPBasicAuth

# Auth
@auth.get_password
def get_password(email):
    users = User.query.filter_by(email=email).first()
    if users is not None:
        return users.password
    return None

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
    username = request.form['username']
    password = request.form['password']
    response = requests.post(url_for(auth_login(username, password)), data={}, auth=(username, password))
    if response.status_code == 200:
        return render_template('Home.html')

@app.route('/loginAuth', methods=['POST'])
@auth.login_required
def auth_login(username, password):
    resp = not_implimented()
    user = User.query.filter_by(email=username).first()
    if request.method == 'POST':
        if user is None:
            resp = jsonify(message= {
                'status': 400,
                'message':"User Not Found",
            }),400
        else:
            if password != user.password:
                resp = jsonify(message= {
                    'status': 400,
                    'message':"Wrong Password",
                }),400
            elif username == user.email and password == user.password:
                session['logged_in'] = True
                session['user'] = user.id
                resp = jsonify(message= {
                    'status': 200,
                    'message':"Logged In!",
                }),200
    return resp

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user', None)
    return redirect(url_for('home'))