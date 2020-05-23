"""
    discord/api.py - Handles connections to Discord.

    This module handles connections to discord. It's
    written because existing library are more suitable
    for bots and we only need a small subset of calls.
"""

import requests

class DiscordAPI:
    def __init__(self, authorization_token):
        self.api_endpoint = 'https://discordapp.com/api'
        self.headers = {'Authorization': authorization_token}

    def build_url(self, *paths):
        return '/'.join([self.api_endpoint, *paths])

    def get_current_user_id(self):
        current_user_url = self.build_url('users', '@me')
        return requests.get(current_user_url, headers=self.headers).json()['id']

    def get_user_channels(self, is_guild):
        user_dms_url = self.build_url('users', '@me', 'guilds' if is_guild else 'channels')
        return requests.get(user_dms_url, headers=self.headers).json()

    def search(self, channel_id, author_id, offset, is_guild):
        search_url = self.build_url(
            'guilds' if is_guild else 'channels',
            channel_id,
            'messages',
            'search?author_id={}'.format(author_id)
        )

        if offset:
            search_url = '{}&offset={}'.format(search_url, offset)

        return requests.get(search_url, headers=self.headers)

    def delete_message(self, channel_id, message_id):
        message_url = self.build_url('channels', channel_id, 'messages', message_id)
        return requests.delete(message_url, headers=self.headers)
