import os
from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)

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
	items = Item.query.order_by(Item.id).all()
	return render_template('Home.html', items = items)

if __name__ == '__main__':
	app.run(debug=True)