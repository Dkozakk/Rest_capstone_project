from flask import request
from flask.json import jsonify
from rest_project import app
from rest_project.models.center import Center, JWTAccess

import jwt
from datetime import datetime, timedelta

def generate_expire_date():
    expire_date = datetime.now() + timedelta(days=2)
    return expire_date


def jwt_required(func):
    def inner(*args, **kwargs):
        token = request.args.get('token')
        try:
            data = jwt.decode(token, key=app.config['SECRET_KEY'])
            center = Center.query.get(data.get('center'))
            center.jwt_accesses.append(JWTAccess())
            return func(center, *args, **kwargs)
        except jwt.DecodeError:
            return jsonify({"Error": "Tokin is not valid"}), 401
    return inner