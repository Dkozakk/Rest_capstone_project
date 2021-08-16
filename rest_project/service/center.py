from rest_project import app, db
from rest_project.models.center import Center
from rest_project.utils.jwt_utils import generate_expire_date

from flask import jsonify, Response

from werkzeug.security import generate_password_hash, check_password_hash

import jwt


def get_all_centers():
    return jsonify([f"{center.login} - {center.id}" for center in Center.query.all()])


def get_center_by_id(id):
    center = Center.query.get(id)
    app.logger.info(f'GETTING CENTER WITH ID {id}')
    if center:
        app.logger.info('SUCCESS!')
        return jsonify({"Center": center.login, "animals": center.get_animals_names()})
    app.logger.error(f'ERROR, CENTER WITH ID {id} DOES NOT EXIST')
    return Response(f"Error, center with id {id} does not exist", 404)


def register_center(login, password, address):
    hashed_password = generate_password_hash(password)
    app.logger.info('CREATING CENTER')
    if login and password and address:
        center = Center(login=login, password=hashed_password, address=address)
        db.session.add(center)
        db.session.commit()
        app.logger.info('CENTER CREATED')
        return Response("Center was created", 201)
    app.logger.error("CENTER WASN'T CREATED, ONE OR MORE FIELDS WAS EMPTY")
    return Response("Error, you didn't provide login, password or address ")


def get_jwt_token(login, password):
    if not login or not password:
        return Response("Login or password is epcent")
    center = Center.query.filter_by(login=login).first()
    if not center:
        return Response("Center with provided login does not exist")
    if not check_password_hash(center.password, password):
        return Response("Password incorrect")
    return jwt.encode({'exp': generate_expire_date(), "center": center.id}, key=app.config['SECRET_KEY'])