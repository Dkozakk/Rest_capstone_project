from rest_project import app
from rest_project.models.animals_models import Animal, Specie
from rest_project.service.animals import (
                                            get_all_animals, 
                                            create_new_animal, 
                                            create_new_specie, 
                                            get_all_species, 
                                            get_animal_by_id, 
                                            edit_animal, 
                                            remove_animal,
                                            get_specie_by_id
                                        )
from rest_project.utils.jwt_utils import jwt_required

from flask import request

import json


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
    return create_animal()


@jwt_required
def create_animal(center):
    data = request.get_json() or json.loads(request.get_data())
    name = data.get('name')
    description = data.get('name')
    age = data.get('age')
    price = data.get('price')
    specie = data.get('specie')
    response = create_new_animal(name=name, age=age, description=description, price=price, specie=specie, center=center)
    return response


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
    return create_specie()


@jwt_required
def create_specie(center):
    data = request.get_json() or json.loads(request.get_data())
    name = data.get('name')
    description = data.get('description', '')
    response = create_new_specie(name=name, description=description)
    return response


def get_animal(id):
    animal_or_response = get_animal_by_id(id)
    return animal_or_response


def put_animal(id):
    data = request.get_json() or json.loads(request.get_data())
    name = data['name']
    price = data['price']
    description = data['description']
    age = data['age']
    specie = data['specie']
    response = edit_animal(id=id, name=name, price=price, description=description, specie=specie, age=age)
    return response


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
    if  request.method == 'GET': 
        return get_animal(id)
    elif request.method == 'PUT': 
        return put_animal(id)
    elif request.method == 'DELETE': 
        return jwt_required(delete_animal)(id=id)


@app.route('/specie/<int:id>', methods=['GET'])
def specie(id):
    """
    rest api endpoint
    GET:
        return detailed view of this Specie with list of animals  
        in format “animal name - id - specie”
    """
    specie_or_response = get_specie_by_id(id)
    return specie_or_response


__all__ = ["species", "animals", "animal", "specie"]