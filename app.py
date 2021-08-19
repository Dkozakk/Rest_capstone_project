from rest_project import app, db

from rest_project.rest.center_api import login, register, get_center, get_centers
from rest_project.rest.animals_api import animal, animals, specie, species

from flask import has_request_context, request

from configparser import ConfigParser

import logging
from datetime import date

import os


@app.before_first_request
def init_db():
    db.create_all()


if __name__ == '__main__':
    try:
        path_to_logs = os.path.join(os.path.dirname(__file__), 'logs')

        logger = logging.getLogger(__name__)
        
        try:
            os.mkdir(os.path.join(path_to_logs))
        except FileExistsError:
            # skip if directory exists
            pass 

        file_handler = logging.FileHandler(filename=os.path.join(path_to_logs, f'logs_{date.today()}'))
        logger.addHandler(file_handler)
        file_handler.setFormatter(logging.Formatter('%(asctime)s | %(message)s'))
        file_handler.setLevel(logging.DEBUG)

        parser = ConfigParser()
        parser.read('config.ini')
        settings = parser['app']
        app.run(port=int(settings.get('port', 5000)), debug=bool(settings.get('debug', False)))
    
    except Exception as e:
        app.logger.error(e)
