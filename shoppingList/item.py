import math
from flask import render_template, request, redirect, url_for, session, jsonify
from shoppingList import app, db, auth, not_implimented
from shoppingList.models import User, List, Item, UserList
"""
Endpoints involving Item
"""

@app.route('/api/item', methods=['POST'])
@auth.login_required
def item_json():
    resp = not_implimented()
    if request.method == 'POST':
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
        resp = jsonify(message), 201
    return resp

@app.route('/api/item/<int:id>', methods=['DELETE'])
@auth.login_required
def delete_item_json(id):
    resp = not_implimented()
    if request.method == 'DELETE':
        item = Item.query.filter_by(id = id).first()
        db.session.delete(item)
        db.session.commit()

        message = {
            'status': 204,
            'message': 'Deleted',
        }
        resp = jsonify(message), 204
    return resp

@app.route('/api/list/item<int:id>', methods=['GET'])
@auth.login_required
def json_list(id):
    resp = not_implimented()
    if not session.get('logged_in'):
        return jsonify(data="Credentials Not Found")
    elif request.method == 'GET':
        items = Item.query.filter_by(list_id = id).all()
        resp = jsonify(data=[i.serialize for i in items]), 201
    return resp