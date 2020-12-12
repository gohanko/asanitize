import unittest
from sanitize.common import random_word, load_yml

class TestCommon(unittest.TestCase):
    def test_random_word(self):
        words = random_word()
        self.assertEqual(len(words), 2000)

    def test_load_yml(self):
        data = load_yml('./test/test.config.yml')
        self.assertEqual(isinstance(data, object), True)
