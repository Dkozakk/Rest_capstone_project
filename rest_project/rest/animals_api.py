import json

from flask import request
from rest_project import app
from rest_project.service.animals import (
    create_new_animal,
    create_new_specie,
    edit_animal,
    get_all_animals,
    get_all_species,
    get_animal_by_id,
    get_specie_by_id,
    remove_animal,
)
from rest_project.utils.jwt_utils import jwt_required


@app.route('/animals', methods=['GET', 'POST'])
def animals():
    """
    rest api endpoint
    GET request:
        return full list of animals
    POST request:
        create an new animal with all required attrs
    """
    if request.method == 'GET':
        return get_all_animals()
    data = request.get_json() or json.loads(request.get_data())
    return jwt_required(create_animal)(data=data)


def create_animal(center, data):
    return create_new_animal(
        name=data.get('name'),
        age=data.get('age'),
        description=data.get('description'),
        price=data.get('price'),
        specie=data.get('specie'),
        center=center,
    )


@app.route('/species', methods=['POST', 'GET'])
def species():
    """
    rest api endpoint
    GET request:
        return full list of species with count of elements on each species
    POST request:
        create an new specie with all required attrs
    """
    if request.method == 'GET':
        return get_all_species()
    data = request.get_json() or json.loads(request.get_data())
    return jwt_required(create_specie)(data=data)


def create_specie(center, data):
    name = data.get('name')
    description = data.get('description')
    response = create_new_specie(name=name, description=description, center=center)
    return response


def put_animal(center, id, data):
    return edit_animal(
        id=id,
        name=data.get('name'),
        price=data.get('price'),
        description=data.get('description'),
        specie=data.get('specie'),
        age=data.get('age'),
        center=center,
    )


def delete_animal(center, id):
    response = remove_animal(center, id)
    return response


@app.route('/animal/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def animal(id):
    """
    rest api endpoint
    GET:
        return detailed information about an animal
    PUT:
        update value of animal
    DELETE:
        delete animal if center that own
    """
    if request.method == 'GET':
        return get_animal_by_id(id)

    if request.method == 'PUT':
        data = request.get_json() or json.loads(request.get_data())
        return jwt_required(put_animal)(id=id, data=data)

    if request.method == 'DELETE':
        return jwt_required(delete_animal)(id=id)


@app.route('/specie/<int:id>', methods=['GET'])
def specie(id):
    """
    rest api endpoint
    GET:
        return detailed view of this Specie with list of animals
        in format “animal name - id - specie”
    """
    return get_specie_by_id(id)


__all__ = ["species", "animals", "animal", "specie"]
