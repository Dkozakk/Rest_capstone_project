import json

from flask import request
from rest_project import app
from rest_project.service.center import (
    get_all_centers,
    get_center_by_id,
    get_jwt_token,
    register_center,
)


@app.route('/register', methods=['POST'])
def register():
    """
    rest api endpoint
    POST:
        register login and password
    """
    data = request.get_json() or json.loads(request.get_data())
    return register_center(
        login=data.get('login'),
        password=data.get('password'),
        address=data.get('address'),
    )


@app.route('/center/<int:id>', methods=['GET'])
def get_center(id):
    """
    rest api endpoint
    GET:
        return detailed information about center with current “id”
    """
    return get_center_by_id(id)


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
    return get_jwt_token(
        login=data.get('login'),
        password=data.get('password'),
    )


__all__ = ["login", "get_center", "register", "get_centers"]
