from shoppingList import app
from flask import render_template, request, redirect, url_for, session


@app.route('/')
def home():
    if not session.get('logged_in'):
    	return render_template('login.html')
    else:
		items = Item.query.order_by(Item.id).all()
		return render_template('Home.html', items = items)

@app.route('/register')
def register():
	user = User(request.form['email'], request.form['password'])

@app.route('/new', methods=['POST'])
def add_item():
	if not session.get('logged_in'):
		return render_template('login.html')
	else:
		item = Item(request.form['name'], request.form['quantity'])
		db.session.add(item)
		db.session.commit()
		return redirect(url_for('home'))

@app.route('/delete', methods=['POST'])
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
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid Username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid Password'
        else:
            session['logged_in'] = True
            return redirect(url_for('home'))
    return render_template('login.html', error = error)