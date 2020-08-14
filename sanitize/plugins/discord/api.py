import time
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