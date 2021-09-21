import json
import unittest

from rest_project import app, db
import rest_project.models.animals_models
from rest_project.models.center_models import Center
import rest_project.rest.center_api

headers = {"Content-type": "application/json"}


class TestCenters(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        app.config['TESTING'] = True
        self.app = app.test_client()

        with app.app_context():
            db.create_all()

        data = {
            "login": "test",
            "password": "test_pswd",
            "address": "address"
        }
        self.app.post('/register', headers=headers, json=data)
        response = self.app.get('/login', headers=headers, json=data)
        self.jwt = response.data.decode('utf-8')

    def test_get_center_by_id(self):
        id = 1
        center = Center.query.get(id)
        response = self.app.get(f'/center/{id}')
        center_from_api = json.loads(response.data)
        self.assertEqual(center.login, center_from_api['Center'])
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
