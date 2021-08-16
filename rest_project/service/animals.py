from rest_project import db
from rest_project.models.animals import Animal, Specie

from flask import jsonify, Response


def get_all_animals():
    return jsonify([animal.serialize() for animal in Animal.query.all()])


def get_specie_by_name(specie_name):
    specie = Specie.query.filter_by(name=specie_name).first()
    return specie

def create_new_animal(name, age, description, price, specie, center):
    if not name or not age or not description or not price or not specie:
        return Response("Error, you didn't provide one or more fields")
    specie = get_specie_by_name(specie)
    if not specie:
        return Response("Error, you must create this specie first")
    animal = Animal(name=name, age=age, description=description, price=price)
    animal.specie = specie
    animal.center = center
    db.session.add(animal)
    db.session.commit()
    return Response("Success")


def create_new_specie(name, description):
    if not name or not description:
        return Response("Error, you didn't provide name or description")
    specie = Specie(name=name, description=description)
    db.session.add(specie)
    db.session.commit()
    return Response("Success")


def get_specie_by_id(id):
    specie = Specie.query.get(id)
    if not specie:
        return Response("Specie with given id does not exist")
    return jsonify({"specie": specie.serialize(), "animals": [f"{animal.name} - {animal.id} - {specie.name}" for animal in specie.animals]})


def get_all_species():
    species = Specie.query.all()
    return jsonify([{"specie": specie.name, "animals": len(specie.animals)} for specie in species])


def get_animal_by_id(id):
    animal = Animal.query.get(id)
    if not animal:
        return Response("Animal with given id does not exist")
    return jsonify(animal.serialize())


def edit_animal(id, name, description, price, age, specie):
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
    return Response("Success")


def remove_animal(center, id):
    animal = Animal.query.get(id)
    if not animal:
        return Response("Animal with given id does not exist")
    if animal.center == center:
        db.session.delete(animal)
        db.session.commit()
        return Response("Success")
    return Response("Error, this animal is not your own")