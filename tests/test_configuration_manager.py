import unittest
from asanitize.configuration_manager import DiscordConfiguration, RedditConfiguration, ConfigurationManager

class TestDiscordConfiguration(unittest.TestCase):
    def setUp(self):
        self.discord_configuration = DiscordConfiguration()
    
    def testHaveProperFields(self):
        self.discord_configuration.token = 'test'
        self.assertEqual(self.discord_configuration.token, 'test')

        self.discord_configuration.channels_to_sanitize = 'test'
        self.assertEqual(self.discord_configuration.channels_to_sanitize, 'test')
        
        self.discord_configuration.fastmode = False
        self.assertEqual(self.discord_configuration.fastmode, False)

class TestRedditConfiguration(unittest.TestCase):
    def setUp(self):
        self.reddit_configuration = RedditConfiguration()

    def testHaveProperFields(self):
        self.reddit_configuration.client_id = 'test'
        self.assertEqual(self.reddit_configuration.client_id, 'test')

        self.reddit_configuration.client_secret = 'test'
        self.assertEqual(self.reddit_configuration.client_secret, 'test')

        self.reddit_configuration.username = 'test'
        self.assertEqual(self.reddit_configuration.username, 'test')

        self.reddit_configuration.password = 'test'
        self.assertEqual(self.reddit_configuration.password, 'test')

class TestConfigurationManager(unittest.TestCase):
    def setUp(self):
        self.configuration_manager = ConfigurationManager()

    def testLoadConfigNotExist(self):
        hasExitHappened = False
        try:
            self.configuration_manager.load_config('./testdata/doesnotexist.json')
        except SystemExit as error:
            if error.code == 0:
                hasExitHappened = True
        
        self.assertTrue(hasExitHappened)

    def testLoadConfigExist(self):
        data = self.configuration_manager.load_config('./testdata/test_config.json')
        self.assertTrue(data)

        self.assertTrue(self.configuration_manager.discord_config.token, 'test_token')
        self.assertTrue(self.configuration_manager.reddit_config.client_id, 'test_client_id')

    