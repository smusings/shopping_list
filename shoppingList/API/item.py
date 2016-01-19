import math
from shoppingList import app, db
"""
API for the Item Model used in our app
"""

@app.route('/item', methods=['POST'])
def item_json():
    if not session.get('logged_in'):
        return "Credentials Not Found"
    elif request.method == 'POST':
        json_list = request.get_json(silent=True)
        for obj in json_list:
            price = abs(obj['price'])
            quantity = int(abs(obj['quantity']))
            item = Item(obj['name'], obj['list_id'], session.get('user'), price, quantity)
            possibleItem = Item.query.filter(Item.name.ilike(obj['name'])).filter_by(list_id=obj['list_id']).first()
            if possibleItem is not None:
                #calls another item for some reason?!
                print possibleItem.name
                print possibleItem.list_id
                print possibleItem.quantity
                possibleItem.price = price
                possibleItem.quantity = quantity + int(possibleItem.quantity)
                print possibleItem.quantity
            else:
                db.session.add(item)
        db.session.commit()
        return '200'
    else:
        return 'false method detected'

@app.route('/item/<int:id>', methods=['DELETE'])
def item_json(id):
    if not session.get('logged_in'):
        return "Credentials Not Found"
    elif request.method == 'DELETE':
        obj = request.get_json(silent=True)
        item = Item.query.filter_by(id = obj).first()
        db.session.delete(item)
        db.session.commit()
    else:
        return 'false method detected'

@app.route('/list/item<int:id>')
def json_list(id):
    if not session.get('logged_in'):
        return jsonify(data="Credentials Not Found")
    else:
        items = Item.query.filter_by(list_id = id).all()
        return jsonify(data=[i.serialize for i in items])