import json
import unittest

from rest_project import app, db
from rest_project.models.animals_models import Animal, Specie
import rest_project.models.center_models
import rest_project.rest.animals_api

headers = {'Content-type': 'application/json'}


class TestAnimals(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        app.config['TESTING'] = True
        cls.app = app.test_client()

        with app.app_context():
            db.create_all()

        data = {
            'login': 'test20',
            'password': 'test_pswd',
            'address': 'address',
        }
        cls.specie_data = {
            'name': 'dog',
            'description': 'simple dog',
        }
        cls.animal_data = {
            'name': 'dog',
            'description': '',
            'price': '12.94',
            'age': 4,
            'specie': cls.specie_data['name'],
        }
        cls.app.post('/register', headers=headers, json=data)
        response = cls.app.get('/login', headers=headers, json=data)
        cls.jwt = response.data.decode('utf-8')

    def test_create_specie(self):
        response = self.app.post(f'/species?token={self.jwt}', headers=headers, json=self.specie_data)
        self.assertIn(b'created', response.data)

    def test_create_animal(self):
        self.app.post(f'/species?token={self.jwt}', headers=headers, json=self.specie_data)
        response = self.app.post(f'/animals?token={self.jwt}', headers=headers, json=self.animal_data)
        self.assertIn(b'created', response.data)

    def test_get_animals(self):
        self.app.post(f'/species?token={self.jwt}', headers=headers, json=self.specie_data)
        response = self.app.post(f'/animals?token={self.jwt}', headers=headers, json=self.animal_data)
        self.assertIn(b'created', response.data)
        response = self.app.get('/animals')
        animals_from_api = json.loads(response.data)
        animals = Animal.query.all()
        self.assertEqual(len(animals_from_api), len(animals))

    def test_get_species(self):
        response = self.app.post(f'/species?token={self.jwt}', headers=headers, json=self.specie_data)
        self.assertIn(b'created', response.data)
        response = self.app.get('/species')
        species_from_response = json.loads(response.data)
        species = Specie.query.all()
        self.assertEqual(len(species_from_response), len(species))
