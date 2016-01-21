
@app.route('/list', methods=['GET','POST'])
def list():
    if not session.get('logged_in'):
        return "Credentials Not Found"
    elif request.method == 'GET':
        user = session.get('user')
        lst = List.query.outerjoin(UserList, List.id == UserList.list_id).filter(UserList.user_id == user).all()
        return jsonify(data=[i.serialize for i in lst])
    elif request.method == 'POST':
        obj = request.get_json(silent=True)
        possible_list = List.query.filter(List.name.ilike(obj)).filter_by(user_id=session.get('user')).first();
        if possible_list is None or  UserList.query.filter_by(list_id=possible_list.id, user_id=session.get('user')).first() is not None:
            lst = List(obj, session.get('user'))
            db.session.add(lst)
            db.session.commit()
            return "Success"
        else:
            return "List Already Created"
    else:
        return'Bummer'

@app.route('/list/<int:id>', methods=['DELETE'])
def delete_table_json(id):
    if not session.get('logged_in'):
        return "Credentials Not Found"
    else:
        if request.method == 'DELETE':
            #Need to check if list is part of user_list AND move it somewhere else
            user_list = UserList.query.filter_by(user_id=session.get('user'), list_id=id).first()
            if user_list is None:
                lst = List.query.filter_by(id=id).first() #investigate bug where it returns None
                db.session.delete(lst)
            else:
                db.session.delete(user_list)
            db.session.commit()
            return 'Removed!'
        else:
            return 'Wrong Call Type'

@app.route('/shoppingList.json')
def shopping_list():
    if not session.get('logged_in'):
        return "Credentials Not Found"
    else:
        user = session.get('user')
        lst = List.query.outerjoin(UserList, List.id == UserList.list_id).filter(List.user_id == user).all()
        return jsonify(data=[i.serialize for i in lst])