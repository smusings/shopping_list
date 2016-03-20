import math
from flask import render_template, request, redirect, url_for, session, jsonify
from shoppingList import app, db, auth, not_implimented
from shoppingList.models import User, List, Item, UserList
"""
Endpoints involving List
"""

@app.route('/api/list', methods=['GET','POST'])
@auth.login_required
def get_list():
    resp = not_implimented()
    if request.method == 'GET':
        user = session.get('user')
        lst = List.query.outerjoin(UserList, List.id == UserList.list_id).filter_by(user_id = user).all()
        resp = jsonify(data=[i.serialize for i in lst]), 201
    elif request.method == 'POST':
        obj = request.get_json(silent=True)
        lst = List.query.outerjoin(UserList, List.id == UserList.list_id).filter(List.name.ilike(obj)).filter(UserList.user_id == session.get('user')).first()
        if lst is None:
            lst = List(obj, session.get('user'))
            db.session.add(lst)
            kst = List.query.filter_by(creator_id = session.get('user')).order_by(List.id.desc()).first();
            userList = UserList(session.get('user'), kst.id)
            db.session.add(userList)
            db.session.commit()

        message = {
            'status': 201,
            'message': 'Created: '+request.url,
        }
        resp = jsonify(message), 201
    return resp

@app.route('/api/list/<int:id>', methods=['GET', 'DELETE'])
@auth.login_required
def delete_table_json(id):
    resp = not_implimented()
    if request.method == 'GET':
        lst = List.query.filter_by(id=id).first()
        resp = jsonify(name = lst.name), 201
    elif request.method == 'DELETE':
        user_list = UserList.query.filter_by(user_id=session.get('user'), list_id=id).first()
        user_lists = UserList.query.filter_by(list_id=id).all()
        if len(user_lists) <= 1:
            lst = List.query.filter_by(id=id).first()
            db.session.delete(lst)
        db.session.delete(user_list)
        db.session.commit()

        message = {
            'status': 201,
            'message': 'Created: '+request.url,
        }
        resp = jsonify(message)
        resp.status_code = 201
    return resp

@app.route('/api/shoppingList')
@auth.login_required
def shopping_list():
    user = session.get('user')
    lst = List.query.outerjoin(UserList, List.id == UserList.list_id).filter(UserList.user_id == user).all()
    return jsonify(data=[i.serialize for i in lst]), 201

@app.route('/api/registerUser', methods=['POST'])
@auth.login_required
def register_user():
    user = User(request.form['email'], request.form['password'])
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/api/shareList', methods=['POST'])
@auth.login_required
def share_list():
    resp = None
    json_list = request.get_json(silent=True)
    for obj in json_list:
        id=obj['id']
        email = obj['email']
        target = User.query.filter_by(email = email).first()
        if target is not None:
            new_connection = UserList(target.id, id)
            db.session.add(new_connection)
            db.session.commit()
            message = {
                'status': 201,
                'message': 'Your List Has Been Shared'
            }
            resp = jsonify(message), 201
        else:
            message = {
                'status': 201,
                'message': 'User Not Found',
            }
            resp = jsonify(message), 201
    return resp

def check_users(shopping_list):
    users = UserList.query.filter_by(list_id = shopping_list.list_id).all()
    if users is None:
        return False
    else:
        return True