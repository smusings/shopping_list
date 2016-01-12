import math
from shoppingList import app, db
from flask import render_template, request, redirect, url_for, session, jsonify
from shoppingList.models import User, List, Item, UserList

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        lists = []
        if session.get('user'):
            user = session.get('user')
            lst = List.query.filter(List.user_id == user).all()
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

#DBRoutes
@app.route("/newList.json", methods=['POST'])
def add_list():
    if not session.get('logged_in'):
        return "Credentials Not Found"
    else:
        if request.method == 'POST':
            obj = request.get_json(silent=True)
            possible_list = List.query.filter_by(name=obj, user_id=session.get('user')).first();
            if possible_list is None or UserList.query.filter_by(list_id=possible_list.id, user_id=session.get('user')).first() is not None:
                lst = List(obj, session.get('user'))
                db.session.add(lst)
                db.session.commit()
                return "Success"
            else:
                return "List Already Found"
        else:
            return 'No JSON Object'

@app.route('/shoppingList.json')
def shopping_list():
    if not session.get('logged_in'):
        return jsonify(data="Credentials Not Found")
    else:
        user = session.get('user')
        lst = List.query.outerjoin(UserList, List.id == UserList.list_id).filter(List.user_id == user).all()
        return jsonify(data=[i.serialize for i in lst])


@app.route('/list.json/<int:id>')
def json_list(id):
    if not session.get('logged_in'):
        return jsonify(data="Credentials Not Found")
    else:
        items = Item.query.filter_by(list_id = id).all()
        return jsonify(data=[i.serialize for i in items])

@app.route('/newItem.json', methods=['GET', 'POST'])
def new_item_json():
    if not session.get('logged_in'):
        return jsonify(data="Credentials Not Found")
    else:
        if request.method == 'POST':
            json_list = request.get_json(silent=True)
            for obj in json_list:
                price = abs(obj['price'])
                quantity = int(abs(obj['quantity']))
                item = Item(obj['name'], obj['list_id'], session.get('user'), price, quantity)
                possibleItem = Item.query.filter_by(name=obj['name'], list_id=obj['list_id']).first()
                if possibleItem is not None:
                    possibleItem.price = price
                    possibleItem.quantity = quantity + int(possibleItem.quantity)
                else:
                    db.session.add(item)
            db.session.commit()
            return 'Success'
        else:
            return 'No JSON Object'

@app.route('/deleteTable.json/<int:id>', methods=['DELETE'])
def delete_table_json(id):
    if not session.get('logged_in'):
        return jsonify(data="Credentials Not Found")
    else:
        if request.method == 'DELETE':
            user_list = UserList.query.filter_by(user_id=session.get('user'), list_id=id).first()
            if user_list is None:
                lst = List.query.filter_by(id=id).first() #investigate bug where it returns None
                db.session.delete(lst)
            else:
                db.session.delete(user_list)
            db.session.commit()
            return 'Removed!'
        else:
            return 'Wrong Call Type'

@app.route('/deleteItem.json', methods=['POST'])
def delete_item_json():
    if not session.get('logged_in'):
        return jsonify(data="Credentials Not Found")
    else:
        if request.method == 'POST':
            obj = request.get_json(silent=True)
            item = Item.query.filter_by(id = obj).first()
            db.session.delete(item)
            db.session.commit()
            return 'Success'
        else:
            return 'No JSON Object'

@app.route('/registerUser', methods=['POST'])
def register_user():
    user = User(request.form['email'], request.form['password'])
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/shareList', methods=['POST'])
def share_list():
    lst = List.query.filter_by(id = request.form['list_id'])
    if "@" in request.form['target_email']:
        target = User.query.filter_by(email = request.form).first()
        userList = UserList(target.id, lst.id)
        db.session.add(userList)
        db.session.commit()
        return "User Found, list added!"
    else:
        msg = Message("Hello, you have had a list shared with you",
            sender="my@email.com",
            recipients=[request.form['target_email']])
        return "User Not Found. Email Sent!"


@app.route('/login', methods=['GET', 'POST'])
def login():
    user = User.query.filter_by(email=request.form['username']).first()
    error = None
    if request.method == 'POST':
        if user is None:
            error = 'Invalid Email'
        else:
            if request.form['password'] != user.password:
                error = 'Invalid Password'
            elif request.form['username'] == user.email and request.form['password'] == user.password:
                session['logged_in'] = True
                session['user'] = user.id
                return redirect(url_for('home'))
        return render_template('login.html', error = error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user', None)
    return redirect(url_for('home'))