import time
from ..common import random_word
from .api import DiscordAPI

class DiscordRoutines(object):
    def __init__(self, authorization_token):
        self.discord_api = DiscordAPI(authorization_token)
        self.user_id = self.discord_api.get_current_user_id()
        self.sanitize_account()

    def filter_messages_by_author(self, messages, author_id):
        authors_messages = []
        for message in messages:
            if message['author']['id'] == author_id:
                authors_messages.append(message)

        return authors_messages

    def sanitize_account(self):
        dm_channels = self.discord_api.get_user_dms(self.user_id)
        for dm_channel in dm_channels:
            messages = self.discord_api.get_user_dm_messages(dm_channel['id'])

            for message in messages:
                if message['author']['id'] == self.user_id:
                    self.discord_api.delete_message(message['channel_id'], message['id'])
                    print('Deleting : {} by {}'.format(message['id'], message['author']['username']))