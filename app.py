import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object('config')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.dirname(os.path.realpath(__file__))+'/db/eugenet.db'

db = SQLAlchemy(app)

class Item(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(120))
	quantity = db.Column(db.String(120))

	def __init__(self, name, quantity=None):
		self.name = name
		if quantity is None:
			quantity = 1
		self.quantity = quantity

	def __repr__(self):
		return '<Item %r>' %self.name

@app.route('/')
def home():
    if not session.get('logged_in'):
    	return render_template('login.html')
    else:
		items = Item.query.order_by(Item.id).all()
		return render_template('Home.html', items = items)

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

if __name__ == '__main__':
	app.run(debug=True)