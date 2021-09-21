import os
from configparser import ConfigParser

config = ConfigParser()


config['database'] = {
    'database_uri': 'sqlite:////tmp/database.db',
    'track_modifications': False
}

config['app'] = {
    'port': 4567,
    'debug': True
}


with open('rest_project/configs/config.ini', 'w') as config_file:
    config.write(config_file)
