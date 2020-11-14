import time
import requests
from itertools import chain
from sanitize.common import random_word

class DiscordAPI:
    def __init__(self, authorization_token):
        self.api_endpoint = 'https://discordapp.com/api'
        self.headers = {'Authorization': authorization_token}

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
            'search?author_id={}'.format(author_id)
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
            time.sleep(int(response.headers.get('retry-after')) / 1000)
            response = self.edit_message(channel_id, message_id, message)
        
        return response

class Channel:
    def __init__(self, discord_api, channel_id, is_guild):
        self.discord_api = discord_api
        self.channel_id = channel_id
        self.is_guild = is_guild

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
    
    def search_messages_by_user(self, author_id):
        search_page = 0
        user_messages = []

        while True:
            response = self.discord_api.search(self.channel_id, author_id, search_page * 25, self.is_guild)
            print('Looking for messages: [{}] {}'.format(response.status_code, response.json()))

            if response.status_code == 429:
                time.sleep(int(response.headers.get('retry-after')) / 1000)
                continue

            filtered_messages = self.filter_search_result_by_user(
                response.json().get('messages'),
                author_id
            )
            if filtered_messages:
                user_messages.extend(filtered_messages)
                search_page += 1
            else:
                break

        return user_messages

    def sanitize(self, author_id):
        messages = self.search_messages_by_user(author_id)

        print('Found {} messages from {} in {}'.format(len(messages), author_id, self.channel_id))
        for index, message in enumerate(messages):
            print('Editing and deleting ({}/{}) in {}'.format(index + 1, len(messages), self.channel_id))

            self.discord_api.edit_message(message['channel_id'], message['id'], random_word())
            self.discord_api.delete_message(message['channel_id'], message['id'])

class DiscordRoutine:
    def __init__(self, authorization_token):
        self.discord_api = DiscordAPI(authorization_token)
        self.user_id = self.discord_api.get_current_user_id()

    def serialize_channels(self):
        serialized_channels = []

        dm_channels = self.discord_api.get_user_channels(should_get_guild=False).json()
        for dm_channel in dm_channels:
            serialized_channels.append(Channel(self.discord_api, dm_channel['id'], False))
        
        guild_channels = self.discord_api.get_user_channels(should_get_guild=True).json()
        for guild_channel in guild_channels:
            serialized_channels.append(Channel(self.discord_api, guild_channel['id'], True))

        return serialized_channels

    def sanitize_channel(self, channel_id):
        channels = self.serialize_channels()
        for channel in channels:
            if channel.channel_id == channel_id:
                channel.sanitize(self.user_id)

    def sanitize_account(self):
        channels = self.serialize_channels()
        for channel in channels:
            channel.sanitize(self.user_id)
