from rest_project import db, app
from rest_project.models.center_models import Center
from rest_project.utils.jwt_utils import generate_expire_date, jwt_required
from rest_project.service.center import get_center_by_id, get_all_centers, register_center, get_jwt_token

from flask import request, Response, jsonify

from werkzeug.security import generate_password_hash, check_password_hash

import json


@app.route('/register', methods=['POST'])
def register():
    """
    rest api endpoint
    POST:
        register login and password
    """
    data = request.get_json() or json.loads(request.get_data())
    login = data.get('login')
    password = data.get('password')
    address=data.get('address')
    response = register_center(login, password, address)
    return response


@app.route('/center/<int:id>', methods=['GET'])
def get_center(id):
    """
    rest api endpoint
    GET:
        return detailed information about center with current “id”
    """
    center_or_response = get_center_by_id(id)
    return center_or_response


@app.route('/centers', methods=['GET'])
def get_centers():
    """
    rest api endpoint
    GET:
        return full list of all centers in format “name - id”
    """
    return get_all_centers()


@app.route('/login', methods=['GET'])
def login():
    """
    rest api endpoint
    GET:
        return token if login and password are ok
    """
    data = request.get_json() or json.loads(request.get_data())
    login = data.get('login')
    password = data.get('password')
    token_or_response = get_jwt_token(login, password)
    return token_or_response
    

__all__ = ["login", "get_center", "register", "get_centers"]