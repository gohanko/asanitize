import requests

class DiscordAPI(object):
    def __init__(self, authorization_token):
        self.api_endpoint = 'https://discordapp.com/api'
        self.headers = { 'Authorization': authorization_token }

    def build_url(self, *paths):
        return '/'.join([self.api_endpoint, *paths])

    def get_current_user_id(self):
        current_user_url = self.build_url('users', '@me')
        return requests.get(current_user_url, headers=self.headers).json()['id']

    def get_user_guilds(self, author_id):
        user_guilds_url = self.build_url('users', '@me', 'guilds')
        return requests.get(user_guilds_url, headers=self.headers).json()

    def get_user_dms(self, author_id):
        user_dms_url = self.build_url('users', '@me', 'channels')
        return requests.get(user_dms_url, headers=self.headers).json()
  
    def search_guild(self, channel_id, author_id, offset=25):
        search_url = self.build_url('guilds', channel_id, 'messages', 'search?author={}&offset={}'.format(author_id, offset))
        return requests.get(search_url, headers=self.headers)

    def search_dm(self, channel_id, author_id, offset=25):
        search_url = self.build_url('channels', channel_id, 'messages', 'search?author={}&offset={}'.format(author_id, offset))
        return requests.get(search_url, headers=self.headers)

    def delete_message(self, channel_id, message_id):
        message_url = self.build_url('channels', channel_id, 'messages', message_id)
        return requests.delete(message_url, headers=self.headers)