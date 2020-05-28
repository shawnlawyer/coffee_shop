import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the database
'''
# db_drop_and_create_all()


@app.route('/drinks')
def get_drinks():
    """Get Drink records short

    """

    response = {
        "success": True,
        "drinks": [drink.short() for drink in Drink.query.all()]
    }

    return jsonify(response), 200


@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_detail():
    """Get Drink records detail

    """

    response = {
        "success": True,
        "drinks": [drink.long() for drink in Drink.query.all()]
    }

    return jsonify(response), 200


@app.route('/drinks', methods=["POST"])
@requires_auth('post:drinks')
def post_drinks():
    """Creates a Drink record

    """

    try:

        values = request.get_json()

        kwargs = {
            "title": values.get('title'),
            "recipe": json.dumps(values.get('recipe'))
        }

        drink = Drink(**kwargs)

        drink.insert()

        response = {
            "success": True,
            "drinks": [drink.long()]
        }

        return jsonify(response), 200

    except:

        abort(422)


@app.route('/drinks/<int:id>', methods=["PATCH"])
@requires_auth('patch:drinks')
def patch_drinks(id):
    """Update a Drink record

    :param id: record id
    :type id: int

    """

    drink = Drink.query.filter(Drink.id == id).first_or_404()

    try:

        values = request.get_json()

        drink.title = values.get('title')
        drink.recipe = json.dumps(values.get('recipe'))

        drink.update()

        response = {
            "success": True,
            "drinks": [drink.long()]
        }

        return jsonify(response), 200

    except:

        abort(422)


@app.route('/drinks/<int:id>', methods=["DELETE"])
@requires_auth('delete:drinks')
def delete_drinks(id):
    """Delete a Drink record

    :param id: record id
    :type id: int

    """

    drink = Drink.query.filter(Drink.id == id).first_or_404()

    try:

        drink.delete()

        response = {
            "success": True,
            "delete": id
        }

        return jsonify(response), 200

    except:

        abort(422)


@app.after_request
def after_request(response):

    response.headers.add(
        'Access-Control-Allow-Headers',
        'Content-Type,Authorization,true'
    )
    response.headers.add(
        'Access-Control-Allow-Methods',
        'GET,PATCH,POST,DELETE,OPTIONS'
    )

    return response


@app.errorhandler(400)
def invalid_claims(error):
    '''
    Error handler for expected error 400.
    '''

    return jsonify({
        "success": False,
        "error": 400,
        "message": "invalid claims",
    }), 400


@app.errorhandler(401)
def invalid_token(error):
    '''
    Error handler for expected error 401.
    '''

    return jsonify({
        "success": False,
        "error": 401,
        "message": "invalid token",
    }), 401


@app.errorhandler(403)
def unauthorized(error):
    '''
    Error handler for expected error 403.
    '''

    return jsonify({
        "success": False,
        "error": 403,
        "message": "unauthorized",
    }), 403


@app.errorhandler(404)
def not_found(error):
    '''
    Error handler for expected error 404.
    '''

    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found",
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    '''
    Error handler for expected error 405.
    '''

    return jsonify({
        "success": False,
        "error": 405,
        "message": "method not allowed",
    }), 405


@app.errorhandler(422)
def unprocessable(error):
    '''
    Error handler for expected error 422.
    '''

    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable",
    }), 422
