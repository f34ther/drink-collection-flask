from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Drink, drink_schema, drinks_schema

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/drinks', methods=['POST'])
@token_required
def create_drink(current_user_token):
    base = request.json['base']
    amount_of_base = request.json['amount_of_base']
    mixer = request.json['mixer']
    amount_of_mixer = request.json['amount_of_mixer']
    blend = request.json['blend']
    user_token = current_user_token.token

    print(f'Test: {current_user_token}')

    drink = Drink(base, amount_of_base, mixer, amount_of_mixer, blend, user_token=user_token)

    db.session.add(drink)
    db.session.commit()

    response = drink_schema.dump(drink)
    return jsonify(response)


@api.route('/drinks', methods=['GET'])
@token_required
def get_recipes(current_user_token):
    a_user = current_user_token.token
    drinks = Drink.query.filter_by(user_token=a_user).all()
    response = drinks_schema.dump(drinks)
    return jsonify(response)


@api.route('/drinks/id', methods=['GET'])
@token_required
def get_single_recipe(current_user_token, id):
    drink = Drink.query.get(id)
    drink.user_token = current_user_token.token
    response = drink_schema.dump(drink)
    return jsonify(response)


@api.route('/drinks/<id>', methods=['PUT'])
@token_required
def update_drink(current_user_token, id):
    drink = Drink.query.get(id)
    drink.base = request.json['base']
    drink.amount_of_base = request.json['amount_of_base']
    drink.mixer = request.json['mixer']
    drink.amount_of_mixer = request.json['amount_of_mixer']
    drink.blend = request.json['blend']

    db.session.commit()
    response = drink_schema.dump(drink)
    return jsonify(response)


@api.route('/drinks/<id>', methods=['DELETE'])
@token_required
def delete_drink(current_user_token, id):
    drink = Drink.query.get(id)
    drink.user_token = current_user_token.token
    db.session.delete(drink)
    db.session.commit()
    response = drink_schema.dump(drink)
    return jsonify(response)
