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
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
# db_drop_and_create_all()

## ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks')
def get_drinks():
    """Get Drink records short

    """

    response = {
        "success": True,
        "drinks": [ drink.short() for drink in Drink.query.all() ]
    }

    return jsonify(response), 200

'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''

@requires_auth('get:drinks-detail')
@app.route('/drinks-detail')
def get_drinks_detail():
    """Get Drink records detail

    """

    response = {
        "success": True,
        "drinks": [ drink.long() for drink in Drink.query.all() ]
    }

    return jsonify(response), 200

'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''

@requires_auth('post:drinks')
@app.route('/drinks', methods=["POST"])
def post_drinks():
    """Creates a Drink record

    """

    try:

        values = request.get_json()

        kwargs = {
            "title" : values.get('title'),
            "recipe" : json.dumps(values.get('recipe'))
        }

        drink = Drink(**kwargs)

        drink.insert()


        response = {
            "success": True,
            "drinks": [ drink.long() ]
        }

        return jsonify(response), 200

    except:

        abort(422)

'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''

@requires_auth('patch:drinks')
@app.route('/drinks/<int:id>', methods=["PATCH"])
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
            "drinks": [ drink.long() ]
        }

        return jsonify(response), 200

    except:

        abort(422)

'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''

@requires_auth('delete:drinks')
@app.route('/drinks/<int:id>', methods=["DELETE"])
def delete_drinks(id):
    """Delete a Drink record

    :param id: record id
    :type id: int

    """

    drink = Drink.query.filter(Drink.id == id).first_or_404()

    try:

        drink.delete()

        response = {
            "success" : True,
            "delete": id
        }

        return jsonify(response), 200

    except:

        abort(422)

## Error Handling

'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above 
'''


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above 
'''

@app.after_request
def after_request(response):

    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')

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
