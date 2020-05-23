"""
    discord/routines.py - Handles our application logic.

    This module handles the routines that we need to
    sanitize a discord account.
"""

import time
from itertools import chain
from .api import DiscordAPI

class DiscordRoutines:
    def __init__(self, authorization_token):
        self.discord_api = DiscordAPI(authorization_token)
        self.user_id = self.discord_api.get_current_user_id()
        self.sanitize_account()

    def filter_search_result_by_user(self, message_groups, author_id):
        if not message_groups:
            return None

        messages = list(chain.from_iterable(message_groups))

        messages_seen = []
        author_messages = []
        for message in messages:
            if message['author']['id'] == author_id and message['id'] not in messages_seen:
                author_messages.append(message)
                messages_seen.append(message['id'])

        return author_messages

    def get_author_messages_by_search_result(self, channel_id, author_id, is_guild):
        search_page = 0
        author_messages = []

        while True:
            response = self.discord_api.search(channel_id, author_id, search_page * 25, is_guild)
            if response.status_code == 429:
                time.sleep(response.retry_after)
                continue

            filtered_messages = self.filter_search_result_by_user(
                response.json().get('messages'),
                author_id
            )
            if filtered_messages:
                author_messages.extend(filtered_messages)
                search_page += 1
            else:
                break

        return author_messages

    def sanitize_account(self):
        dm_channels = self.discord_api.get_user_channels(False)
        for dm_channel in dm_channels:
            messages = self.get_author_messages_by_search_result(
                dm_channel['id'],
                self.user_id,
                False
            )

            for message in messages:
                self.discord_api.delete_message(message['channel_id'], message['id'])
                print('Deleting {}: {}'.format(message['id'], message['content']))

        guild_channels = self.discord_api.get_user_channels(True)
        for guild_channel in guild_channels:
            messages = self.get_author_messages_by_search_result(
                guild_channel['id'],
                self.user_id,
                True
            )

            for message in messages:
                self.discord_api.delete_message(message['channel_id'], message['id'])
                print('Deleting {}: {}'.format(message['id'], message['content']))
