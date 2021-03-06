from shoppingList import db, auth
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))

    def __init__(self, email, password):
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, name, creator):
        self.name = name
        self.creator_id = creator

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'creator_id': self.creator_id
        }

class UserList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    list_id = db.Column(db.Integer, db.ForeignKey('list.id'))

    def __init__(self, userId, listId):
        self.user_id = userId
        self.list_id = listId

    @property
    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'list_id': self.list_id
        }

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    quantity = db.Column(db.String(120))
    price = db.Column(db.Integer)
    checked = db.Column(db.Boolean)
    list_id = db.Column(db.Integer, db.ForeignKey('list.id'))

    def __init__(self, name, listId, price=None, quantity=None):
        self.name = name
        self.list_id = listId
        self.checked = False
        if price is None:
            price = 0
        self.price = price;
        if quantity is None:
            quantity = 1
        self.quantity = quantity

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'list_id': self.list_id,
            'price': self.price,
            'checked': self.checked,
            'quantity': self.quantity,
        }