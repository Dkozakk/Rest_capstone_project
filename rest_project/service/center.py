from sqlite3.dbapi2 import IntegrityError

import jwt
from flask import Response, jsonify
from rest_project import app, db
from rest_project.models.center_models import Center
from rest_project.utils.checking_utils import check_center_attributes
from rest_project.utils.jwt_utils import generate_expire_date
from werkzeug.security import check_password_hash, generate_password_hash


def get_all_centers():
    """
    function for get all centers from database
    return:
        detailed information about center in json format
    """
    return jsonify([f"{center.login} - {center.id}" for center in Center.query.all()])


def get_center_by_id(id):
    """
    function get center by id from database
    return:
        Error response
        detailed information about center with current id in json format
    """
    center = Center.query.get(id)
    app.logger.info(f'GETTING CENTER WITH ID {id}')
    if not center:
        app.logger.error(f'ERROR, CENTER WITH ID {id} DOES NOT EXIST')
        return Response(f"Error, center with id {id} does not exist", 404)
    
    app.logger.info('SUCCESS!')
    return jsonify({"Center": center.login, "animals": center.get_animals_names()})


def register_center(login, password, address):
    """
    function create new center and save into db
    attrs:
        login: str centers name
        password: str centers password
        address: str centers address
    return:
        Error response
        Success response
    """
    if not any((login, password, address)):
        app.logger.error("CENTER WASN'T CREATED, ONE OR MORE FIELDS WAS EMPTY")
        return Response("Error, you didn't provide login, password or address ")
    
    checked, msg = check_center_attributes(login=login, password=password, address=address)
    if not checked:
        return Response(msg)

    hashed_password = generate_password_hash(password)
    
    try:
        center = Center(login=login, password=hashed_password, address=address)
        db.session.add(center)
        db.session.commit()
    except Exception:
        return Response("Center whith this name already exists")
    app.logger.info('CENTER CREATED')
    return Response("Center was created", 201)


def get_jwt_token(login, password):
    """
    function creating new jwt token for center
    attrs:
        login: centers login
        password: centers password
    return:
        Error response
        jwt token
    """
    if not login or not password:
        return Response("Login or password is epcent")
    
    center = Center.query.filter_by(login=login).first()
    
    if not center:
        return Response("Center with provided login does not exist")
    
    if not check_password_hash(center.password, password):
        return Response("Password incorrect")
    return jwt.encode({'exp': generate_expire_date(), "center": center.id}, key=app.config['SECRET_KEY'])
