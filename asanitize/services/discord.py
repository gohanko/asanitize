import time
import sys
import math
import requests
from itertools import chain
from asanitize.common import random_word

class API:
    def __init__(self, authorization_token):
        self.api_endpoint = 'https://discordapp.com/api'
        self.headers = {'Authorization': authorization_token}
        if not self._is_token_valid(authorization_token):
            print('Token is not valid')
            sys.exit(0)

    def _is_token_valid(self, token):
        current_user_url = self.build_url('users', '@me')
        response = requests.get(current_user_url, headers=self.headers)
        return response.status_code != 401

    def build_url(self, *paths):
        return '/'.join([self.api_endpoint, *paths])

    def get_current_user_id(self):
        current_user_url = self.build_url('users', '@me')
        return requests.get(current_user_url, headers=self.headers).json()['id']

    def get_user_channels(self, should_get_guild):
        user_dms_url = self.build_url('users', '@me', 'guilds' if should_get_guild else 'channels')
        return requests.get(user_dms_url, headers=self.headers)

    def get_channel_information(self, channel_id):
        channel_info_url = self.build_url('channels', channel_id)
        return requests.get(channel_info_url, headers=self.headers)

    def search(self, channel_id, author_id, offset, should_search_guild):
        search_url = self.build_url(
            'guilds' if should_search_guild else 'channels',
            channel_id,
            'messages',
            'search?author_id={}&include_nsfw=true'.format(author_id),
        )

        if offset:
            search_url = '{}&offset={}'.format(search_url, offset)

        return requests.get(search_url, headers=self.headers)

    def delete_message(self, channel_id, message_id):
        message_url = self.build_url('channels', channel_id, 'messages', message_id)
        response = requests.delete(message_url, headers=self.headers)

        if response.status_code == 429:
            time.sleep(int(response.headers.get('retry-after')) / 1000) 
            response = self.delete_message(channel_id, message_id)
        
        return response

    def edit_message(self, channel_id, message_id, message):
        message_url = self.build_url('channels', channel_id, 'messages', message_id)

        headers = self.headers
        headers.update({'Content-type': 'application/json'})

        response = requests.patch(
            message_url,
            headers=headers,
            json={'content': message}
        )
        if response.status_code == 429:
            sleep_interval = int(response.headers.get('retry-after')) / 1000
            print('API returned 429, waiting for {} seconds before proceeding...'.format(sleep_interval))
            time.sleep(sleep_interval)
            response = self.edit_message(channel_id, message_id, message)
        
        return response

class Channel:
    def __init__(self, discord_api, channel_name, channel_id, is_guild):
        self.discord_api = discord_api
        self.channel_name = channel_name
        self.channel_id = channel_id
        self.is_guild = is_guild

    def sanitize(self, author_id):
        print('Sanitizing channel: {}'.format(self.channel_name))

        # Make sure total_result is never unqueried.
        total_result = 0
        while total_result == 0:
            total_result = self.discord_api.search(self.channel_id, author_id, 0, self.is_guild).json().get('total_results')

        messages_seen = []
        while True:
            response = self.discord_api.search(self.channel_id, author_id, 0, self.is_guild).json()
            if not response.get('total_results'):
                print('No messages left!')
                break

            messages = list(chain.from_iterable(response.get('messages')))
            for message in messages:
                if message['author']['id'] == author_id and message['id'] not in messages_seen:
                    print('Editing and deleting ({}/{}) in {}'.format(len(messages_seen) + 1, total_result, self.channel_name))
                    self.discord_api.edit_message(message['channel_id'], message['id'], random_word())
                    self.discord_api.delete_message(message['channel_id'], message['id'])
                    messages_seen.append(message['id'])

class DiscordRoutine:
    def __init__(self, authorization_token):
        self.discord_api = API(authorization_token)
        self.user_id = self.discord_api.get_current_user_id()

    def _generate_dm_channel_name(self, channel):
        recipients = []
        for recipient in channel['recipients']:
            recipients.append(recipient['username'])

        channel_name = ', '.join(recipients)
        return 'DM Chat with {}'.format(channel_name)

    def serialize_channels(self):
        serialized_channels = {}

        dm_channels = self.discord_api.get_user_channels(should_get_guild=False).json()
        for dm_channel in dm_channels:
            serialized_channels[dm_channel['id']] = Channel(self.discord_api, self._generate_dm_channel_name(dm_channel), dm_channel['id'], False)
        
        guild_channels = self.discord_api.get_user_channels(should_get_guild=True).json()
        for guild_channel in guild_channels:
            serialized_channels[guild_channel['id']] = Channel(self.discord_api, guild_channel['name'], guild_channel['id'], True)

        return serialized_channels

    def sanitize_channel(self, channel_id):
        channel = self.serialize_channels().get(channel_id)
        channel.sanitize(self.user_id)

    def sanitize_account(self):
        channels = self.serialize_channels()
        for channel in channels.values():
            channel.sanitize(self.user_id)
