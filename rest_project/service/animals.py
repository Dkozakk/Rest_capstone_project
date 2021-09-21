import logging

from flask import Response, jsonify, request
from rest_project import db
from rest_project.models.animals_models import Animal, Specie
from rest_project.utils.checking_utils import (
    check_animal_attributes,
    check_specie_attributes,
)

logger = logging.getLogger('rest_app_logger')

message = "{method} | {url} | Center: {center_id} | {entity_type}: {entity_id}"


def log(center_id, entity_type, entity_id):
    logger.info(message.format(
        method=request.method,
        url=request.url,
        center_id=center_id,
        entity_type=entity_type,
        entity_id=entity_id,
        )
    )


def get_all_animals():
    """
    function for get all animals from database
    return:
        list of all serialized animal in json format
    """
    return jsonify([animal.serialize() for animal in Animal.query.all()])


def get_specie_by_name(specie_name):
    """
    function for get specie by name from database
    attrs:
        specie_name: str name of specie
    return:
        first occurrence specie with name specie_name
    """
    return Specie.query.filter_by(name=specie_name).first()


def create_new_animal(name, age, description, price, specie, center):
    """
    function for creating new animal and save into database
    attrs:
        name: str animals name
        age: int animals age
        description: str animals description
        price: str animals price
        specie: str animals specie name
        center: Center center that owns this animal
    return:
        Error response
        Success response
    """
    if not any((name, age, description, price, specie)):
        return Response("Error, you didn't provide one or more fields")

    checked, msg = check_animal_attributes(name=name, age=age, price=price, description=description)
    if not checked:
        return Response(msg)

    specie = get_specie_by_name(specie)

    if not specie:
        return Response("Error, you must create this specie first")

    animal = Animal(
        name=name,
        age=age,
        description=description,
        price=price,
    )
    animal.specie = specie
    animal.center = center
    db.session.add(animal)
    db.session.commit()
    log(center_id=center.id, entity_type='Animal', entity_id=animal.id)

    return Response("Animal was created")


def create_new_specie(name, description, center):
    """
    function create new specie and save into database
    attrs:
        name: str species name
        description: str species description
        center: Center just for logging
    """
    if not any((name, description)):
        return Response("Error, you didn't provide name or description")

    checked, msg = check_specie_attributes(name=name, description=description)
    if not checked:
        return Response(msg)

    specie = Specie(name=name, description=description)
    db.session.add(specie)
    db.session.commit()
    log(center_id=center.id, entity_type='Specie', entity_id=specie.id)
    return Response("Specie was created")


def get_specie_by_id(id):
    """
    function get specie by id from database
    attrs:
        id: int id for search specie
    return:
        Error response
        specie with animals in json format
    """
    specie = Specie.query.get(id)
    if not specie:
        return Response("Specie with given id does not exist")
    return jsonify({
        "specie": specie.serialize(), 
        "animals": [f"{animal.name} - {animal.id} - {specie.name}" for animal in specie.animals]
        })


def get_all_species():
    """
    function get all species from database
    return:
        list of species with counts animals in json format
    """
    return jsonify([{"specie": specie.name, "animals": len(specie.animals)} for specie in Specie.query.all()])


def get_animal_by_id(id):
    """
    function get animal by id from database
    attrs:
        id: int id for search animal
    return:
        Error response
        serialized animal in format json
    """
    animal = Animal.query.get(id)
    if not animal:
        return Response("Animal with given id does not exist")
    return jsonify(animal.serialize())


def edit_animal(id, name, description, price, age, specie, center):
    """
    function update value of animal in database
    attrs:
        id: int id animal you want to update
        name: str new animals name
        description: str new animals description
        price: str new animals price
        age: int new animals age
        specie: new animals specie
    return:
        Error response
        Success response
    """
    animal = Animal.query.get(id)
    if not animal:
        return Response("Animal with given id does not exist")
    animal.name = name
    animal.description = description
    animal.price = price
    animal.age = age
    specie = get_specie_by_name(specie)
    if not specie:
        return Response("Error, you must create this specie first")
    animal.specie = specie
    db.session.commit()
    log(center_id=center.id, entity_type='Animal', entity_id=id)
    return Response("Animal was updated")


def remove_animal(center, id):
    """
    function delete animal from database
    attrs:
        center: Center center which owns animal
        id: int animals id to delete
    return:
        Error response
        Success response
    """
    animal = Animal.query.get(id)
    if not animal:
        return Response("Animal with given id does not exist")
    if animal.center == center:
        db.session.delete(animal)
        db.session.commit()
        log(center_id=center.id, entity_id=id, entity_type='Animal')
        return Response("Animal was deleted")
    return Response("Error, this animal is not your own")
