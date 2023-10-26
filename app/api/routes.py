from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Entry, entry_schema, entries_schema

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'yee': 'haw'}

@api.route('/entries', methods = ['POST'])
@token_required
def create_entry(current_user_token):
    name = request.json['name']
    date = request.json['date']
    cards = request.json['cards']
    journal_entry = request.json['journal_entry']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    entry = Entry(name, date, cards, journal_entry, user_token = user_token)

    db.session.add(entry)
    db.session.commit()

    response = entry_schema.dump(entry)
    return jsonify(response)

@api.route('/entries', methods = ['GET'])
@token_required
def get_entry(current_user_token):
    a_user = current_user_token.token
    entries = Entry.query.filter_by(user_token = a_user).all()
    response = entries_schema.dump(entries)
    return jsonify(response)

#To get a single entry, id = the id that is automatically assigned by the system when a entry is added
@api.route('/entries/<id>', methods = ['GET'])
@token_required
def get_single_entry(current_user_token, id):
    entry = Entry.query.get(id)
    response = entry_schema.dump(entry)
    return jsonify(response)  

# update entry
@api.route('/entries/<id>', methods = ['POST', 'PUT'])
@token_required
def update_entry(current_user_token, id):
    entry = Entry.query.get(id)
    entry.name = request.json['name']
    entry.date = request.json['date']
    entry.cards = request.json['cards']
    entry.jounral_entry = request.json['journal_entry']
    entry.user_token = current_user_token.token
    
    db.session.commit()
    response = entry_schema.dump(entry)
    return jsonify(response)

# delete entry
@api.route('/entries/<id>', methods = ['DELETE'])
@token_required
def delete_entry(current_user_token, id):
    entry = Entry.query.get(id)
    db.session.delete(entry)
    db.session.commit()
    response = entry_schema.dump(entry)
    return jsonify(response)