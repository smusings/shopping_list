import math
from flask import render_template, request, redirect, url_for, session, jsonify
from shoppingList import app, db
from shoppingList.models import User, List, Item, UserList
"""
Endpoints involving Item
"""

@app.route('/api/item', methods=['POST'])
def item_json():
    if not session.get('logged_in'):
        return "Credentials Not Found"
    elif request.method == 'POST':
        json_list = request.get_json(silent=True)
        for obj in json_list:
            print obj
            price = abs(obj['price'])
            quantity = int(abs(obj['quantity']))
            item = Item(obj['name'], obj['list_id'], session.get('user'), price, quantity)
            possibleItem = Item.query.filter(Item.name.ilike(obj['name'])).filter_by(list_id=obj['list_id']).first()
            if possibleItem is not None:
                possibleItem.price = price
                possibleItem.quantity = quantity + int(possibleItem.quantity)
            else:
                db.session.add(item)
        db.session.commit()

        message = {
            'status': 201,
            'message': 'Created: '+request.url,
        }
        resp = jsonify(message)
        resp.status_code = 201
        return resp
    else:
        message = {
            'status': 501,
            'message': 'Not Implimented',
        }
        resp = jsonify(message)
        resp.status_code = 501
        return resp

@app.route('/api/item/<int:id>', methods=['DELETE'])
def delete_item_json(id):
    if not session.get('logged_in'):
        return "Credentials Not Found"
    elif request.method == 'DELETE':
        item = Item.query.filter_by(id = id).first()
        db.session.delete(item)
        db.session.commit()

        message = {
            'status': 204,
            'message': 'Deleted',
        }
        resp = jsonify(message)
        resp.status_code = 204
        return resp
    else:
        message = {
            'status': 501,
            'message': 'Not Implimented',
        }
        resp = jsonify(message)
        resp.status_code = 501
        return resp

@app.route('/api/list/item<int:id>', methods=['GET'])
def json_list(id):
    if not session.get('logged_in'):
        return jsonify(data="Credentials Not Found")
    else:
        items = Item.query.filter_by(list_id = id).all()
        return jsonify(data=[i.serialize for i in items])
    else:
        message = {
            'status': 501,
            'message': 'Not Implimented',
        }
        resp = jsonify(message)
        resp.status_code = 501
        return resp