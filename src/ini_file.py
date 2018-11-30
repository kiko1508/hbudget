import os.path
import configparser


def is_there_ini_file(file):
    return os.path.isfile(file)


def create_ini_file(file):
    config = configparser.ConfigParser()
    config['DEFAULT'] = {'db_name': 'budget'}
    config['tables'] = {}

    with open(file, 'w') as f:
        config.write(f)


def read_ini_file(file):
    config = configparser.ConfigParser()
    config.read(file)

    return config['DEFAULT']['db_name']

