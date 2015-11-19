from shoppingList import app
from flask import render_template, request, redirect, url_for, session
from shoppingList.models import User, List, Item

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login_lists')
    else:
        user = session.get('user')
        lists = (session.query(List).join(UserList).filter(UserList.user_id == user.id).order_by(UserList.id)).all()
        return render_template('shopping_lists')

@app.route('/register')
def register():
    user = User(request.form['email'], request.form['password'])
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('login'))

@app.route('/newItem', methods=['POST'])
def add_item():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        item = Item(request.form['name'], request.form['quantity'])
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('home'))

@app.route('/deleteItem', methods=['POST'])
def delete_item():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        id = request.form['id']
        item = Item.query.filter_by(id=id).first()
        db.session.delete(item)
        db.session.commit()
        return redirect(url_for('home'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    user = User.query.filter_by(email=request.form['username'])
    error = None
    if request.method == 'POST':
        if user == null:
            error = 'Invalid Email'
        elif user.password != request.form['password']:
            error = 'Invalid Password'
        elif request.form['username'] == user.email and request.form['password'] == user.password:
            session['logged_in'] = True
            session['user'] = user
            return redirect(url_for('home'))
        return render_template('login.html', error = error)