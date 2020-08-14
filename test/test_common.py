import unittest

from sanitize.common import (
    random_word,
    create_logger,
)

class TestCommon(unittest.TestCase):
    def test_random_word(self):
        words = random_word()
        self.assertEqual(len(words), 2000)

    def test_create_logger(self):
        logger = create_logger('test_logger')
        self.assertEqual(isinstance(logger, object), True)
