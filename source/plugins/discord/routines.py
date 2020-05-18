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

    def filter_messages_by_author_from_search(self, message_groups, author_id):
        filtered_messages = []
        for message_group in message_groups:
            messages = self.filter_messages_by_author(message_group, author_id)
            for message in messages:
                if not any(message['id'] == filtered_message['id'] for filtered_message in filtered_messages):
                    filtered_messages.append(message)

        return filtered_messages

    def get_user_messages(self, is_guild, channel_id, author_id, page=0):
        search_response = self.discord_api.search_guild(channel_id, author_id, page * 25) if is_guild else self.discord_api.search_dm(channel_id, author_id, page * 25)
        if search_response.status_code == 429:
            time.sleep(search_response.retry_after)
            yield from self.get_user_messages(is_guild, channel_id, author_id, page)

        messages = self.filter_messages_by_author_from_search(search_response.json()['messages'], author_id)
        if messages:
            yield from messages
            yield from self.get_user_messages(is_guild, channel_id, author_id, page + 1)

        return

    def delete_all_user_messages(self, is_guild, channel_id, author_id):
        for message in self.get_user_messages(is_guild, channel_id, author_id):
            self.discord_api.edit_message(channel_id, message['id'], random_word())
            self.discord_api.delete_message(message['id'])

    def sanitize_account(self):
        dms = self.discord_api.get_user_dms(self.user_id)
        for dm in dms:
            self.delete_all_user_messages(False, dm['id'], self.user_id)

        guilds = self.discord_api.get_user_guilds(self.user_id)
        for guild in guilds:
            self.delete_all_user_messages(True, guild['id'], self.user_id)