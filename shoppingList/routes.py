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
    return render_template('list.html', list_id = id)

#DBRoutes
@app.route('/list.json/<int:id>')
def json_list(id):
    items = Item.query.filter_by(list_id = id).all()
    return jsonify(data=[i.serialize for i in items])

@app.route('/newList', methods=['POST'])
def add_list():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        lst = List(request.form['name'], session.get('user'))
        db.session.add(lst)
        db.session.commit()
        return redirect(url_for('home'))

@app.route('/newItem.json', methods=['GET', 'POST'])
def new_item_json():
    if request.method == 'POST':
        json_list = request.get_json(silent=True)
        obj = json_list[0]
        item = Item(obj['name'], obj['list_id'], obj['quantity'])
        db.session.add(item)
        db.session.commit()
        return 'Success'
    else:
        return 'No JSON Object'

@app.route('/deleteItem.json', methods=['GET', 'POST'])
def delete_item_json():
    if request.method == 'POST':
        obj = request.get_json(silent=True)
        # obj = json_list[0]
        print obj
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

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user', None)
    return redirect(url_for('home'))

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