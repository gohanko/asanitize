import unittest

from sanitize.common import (
    random_word,
    load_yml,
    create_logger,
)

class TestCommon(unittest.TestCase):
    def test_random_word(self):
        words = random_word()
        self.assertEqual(len(words), 2000)

    def test_load_yml(self):
        data = load_yml('./config/test.config.yml')
        self.assertEqual(isinstance(data, object), True)

    def test_create_logger(self):
        logger = create_logger('test_logger')
        self.assertEqual(isinstance(logger, object), True)