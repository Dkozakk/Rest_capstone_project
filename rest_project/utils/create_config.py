from configparser import ConfigParser

import os


config = ConfigParser()


config['database'] = {
    'Database_uri': 'sqlite:////tmp/database.db',
    'Track_modifications': False
}

config['app'] = {
    'Port': 4567,
    'Debug': True
}


os.chdir('.')
print(os.getcwd())
with open('config.ini', 'w') as config_file:
    config.write(config_file)