import unittest
from sanitize.common import load_yml
from sanitize.services.reddit import RedditRoutine

class TestRoutine(unittest.TestCase):
    def test__login(self):
        routine = RedditRoutine('invalid_client_id', 'invalid_client_secret', 'invalid_username', 'invalid_password')
        self.assertEqual(routine.is_logged_in(), False)

        env = load_yml('env.yml')['reddit']
        routine = RedditRoutine(
            env.get('client_id'),
            env.get('client_secret'),
            env.get('username'),
            env.get('password'),
            env.get('2fa'),
        )
        self.assertEqual(routine.is_logged_in(), True)

    def test_sanitize_all(self):
        env = load_yml('env.yml')['reddit']
        routine = RedditRoutine(
            env.get('client_id'),
            env.get('client_secret'),
            env.get('username'),
            env.get('password'),
            env.get('2fa'),
        )
        self.assertEqual(routine.sanitize_all(), True)

