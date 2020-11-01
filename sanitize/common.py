import random
import string
import logging
import logging.config

import yaml

def random_word():
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(2000))

def load_yml(file_path):
    with open(file_path, 'r') as yml_file:
        data = yaml.safe_load(yml_file.read())

    return data

def create_logger(name):
    config = load_yml('./config/logging_config.yaml')
    logging.config.dictConfig(config)

    return logging.getLogger(name)
