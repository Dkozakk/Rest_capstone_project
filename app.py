from rest_project import app, db

from rest_project.rest.center import *
from rest_project.rest.animals import *

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
        try:
            os.mkdir(os.path.join(path_to_logs))
        except FileExistsError:
            pass
        logging.basicConfig(filename=os.path.join(path_to_logs, f'logs_{date.today()}'), format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
        app.logger.info('RUNNING SERVER')
        parser = ConfigParser()
        parser.read('config.ini')
        settings = parser['app']
        app.run(port=int(settings.get('port', 5000)), debug=bool(settings.get('debug', False)))
    finally:
        app.logger.info('STOPPING SERVER')