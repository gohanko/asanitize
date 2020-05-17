import requests

class DiscordAPI(object):
    def __init__:
        self.api_endpoint = 'https://discordapp.com/api/v6'
        self.headers = { 'Authorization': authorization_token }

    def build_url(self, *paths):
        return self.api_endpoint.join('/', paths)

    def search_guild(self, channel_id, author_id, offset=25):
        search_url = self.build_url('guilds', channel_id, 'messages', 'search?author={}&offset={}'.format(author_id, offset))
        return requests.get(search_url, self.headers)

    def search_dm(self, channel_id, author_id, offset=25):
        search_url = self.build_url('channels', channel_id, 'messages', 'search?author={}&offset={}'.format(author_id, offset))
        return requests.get(search_url, self.headers)

    def delete_message(self, channel_id, message_id):
        message_url = self.build_url('channels', channel_id, 'messages', message_id)
        return requests.delete(message_url, headers=self.headers)