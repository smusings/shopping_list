from flask.ext.sqlalchemy import SQLAlchemy
from shoppingList import db

class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	email = db.Column(db.String(255), unique = True)
	password = db.Column(db.String(255))

	def __init__(self, email, password):
		self.email = email
		self.password = password

class List(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __init__(self, id, userId):
		self.user_id = userId

class Item(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(120))
	quantity = db.Column(db.String(120))
	list_id = db.Column(db.Integer, db.ForeignKey('list.id'))

	def __init__(self, name, listId, quantity=None):
		self.name = name
		self.list_id = listId
		if quantity is None:
			quantity = 1
		self.quantity = quantity