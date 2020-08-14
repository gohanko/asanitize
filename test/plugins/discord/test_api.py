import unittest
from unittest import mock

from sanitize.plugins.discord.api import DiscordAPI

# TODO: we have to do something about the duplications in this file.
def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data
    
    url = args[0]
    if url == 'https://discordapp.com/api/users/@me':
        return MockResponse({ 'id': 'TestID'}, 200)
    elif url == 'https://discordapp.com/api/users/@me/channels':
        return MockResponse([
            { 'id': '0000' },
            { 'id': '0001' },
        ], 200)
    elif url == 'https://discordapp.com/api/users/@me/guilds':
        return MockResponse([
            { 'id': '0002' },
            { 'id': '0004' },
        ], 200)

    return MockResponse(None, 404)

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.discord_api = DiscordAPI('fakeauthtoken')

    def test_build_url(self):
        url = self.discord_api.build_url('test', 'url')
        self.assertEqual(url, 'https://discordapp.com/api/test/url')

    # TODO: maybe we don't need mock_get
    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_get_current_user_id(self, mock_get):
        current_user_id = self.discord_api.get_current_user_id()
        self.assertEqual(current_user_id, 'TestID')

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_get_user_channels(self, mock_get):
        dm_channels = self.discord_api.get_user_channels(should_get_guild=False)
        for dm_channel in dm_channels:
            self.assertEqual('id' in guild_channel, True)
            self.assertEqual(bool(dm_channel['id']), True)

        guild_channels = self.discord_api.get_user_channels(should_get_guild=True).json()
        for guild_channel in guild_channels:
            self.assertEqual('id' in guild_channel, True)
            self.assertEqual(bool(guild_channel['id']), True)
