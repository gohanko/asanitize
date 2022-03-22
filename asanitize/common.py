import random
import string
import yaml


def random_word():
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(2000))


def load_config_from_file(file_path, service):
    with open(file_path, 'r') as yml_file:
        config = yaml.safe_load(yml_file.read())

    return config.get(service)
