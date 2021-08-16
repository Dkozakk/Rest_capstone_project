from rest_project import app
from rest_project.models.animals import Animal, Specie
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


@app.route('/animals', methods=['GET', 'POST'])
def animals():
    if request.method == 'GET':
        return get_animals()
    return create_animal()


def get_animals():
    return get_all_animals()


@jwt_required
def create_animal(center):
    data = request.get_json()
    name = data.get('name')
    description = data.get('name')
    age = data.get('age')
    price = data.get('price')
    specie = data.get('specie')
    response = create_new_animal(name=name, age=age, description=description, price=price, specie=specie, center=center)
    return response


@app.route('/species', methods=['POST', 'GET'])
def species():
    if request.method == 'GET':
        return get_species()
    return create_specie()

def get_species():
    return get_all_species()

@jwt_required
def create_specie(center):
    data = request.get_json()
    name = data.get('name')
    description = data.get('description', '')
    response = create_new_specie(name=name, description=description)
    return response


def get_animal(id):
    animal_or_response = get_animal_by_id(id)
    return animal_or_response


def put_animal(id):
    data = request.get_json()
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
    if  request.method == 'GET': 
        return get_animal(id)
    elif request.method == 'PUT': 
        return put_animal(id)
    elif request.method == 'DELETE': 
        return jwt_required(delete_animal)(id=id)


@app.route('/specie/<int:id>', methods=['GET'])
def specie(id):
    specie_or_response = get_specie_by_id(id)
    return specie_or_response


__all__ = ["species", "animals", "animal", "specie"]