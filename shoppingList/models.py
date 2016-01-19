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
	name = db.Column(db.String(255))

	def __init__(self, name, userId):
		self.name = name

	@property
	def serialize(self):
		return {
			'id' : self.id,
			'name':self.name
		}

class UserList(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	list_id = db.Column(db.Integer, db.ForeignKey('list.id'))

	def __init__(self, userId, listId):
		self.user_id = userId
		self.list_id = listId

	@property
	def serialize(self):
		return {
			'id' : self.id,
			'user_id':user_id,
			'list_id':list_id,
		}

class Item(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(120))
	quantity = db.Column(db.String(120))
	price = db.Column(db.Integer)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	list_id = db.Column(db.Integer, db.ForeignKey('list.id'))

	def __init__(self, name, listId, user_id, price=None, quantity=None):
		self.name = name
		self.list_id = listId
		self.user_id = user_id
		if price is None:
			price = 0
		self.price = price;
		if quantity is None:
			quantity = 1
		self.quantity = quantity

	@property
	def serialize(self):
		return {
			'id' : self.id,
			'name':self.name,
			'list_id':self.list_id,
			'price':self.price,
			'user_id':self.user_id,
			'quantity':self.quantity,
		}