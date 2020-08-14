import logging
import logging.config
import yaml

def create_logger(name):
    with open('./logging_config.yaml', 'r') as file_handler:
        config = yaml.safe_load(file_handler.read())
        logging.config.dictConfig(config)

    logger = logging.getLogger(name)
    return logger