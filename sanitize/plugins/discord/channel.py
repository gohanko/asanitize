import time

from itertools import chain

from sanitize.common import random_word
from sanitize.logger import create_logger

class Channel:
    def __init__(self, discord_api, channel_id, is_guild):
        self.discord_api = discord_api
        self.channel_id = channel_id
        self.logger = create_logger(__name__)
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
            self.logger.debug(
                '%s - %s - %s',
                self.search_messages_by_user.__name__,
                response.status_code,
                response.json()
            )
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

        self.logger.info('Found %s messages from %s on %s.', len(messages), author_id, self.channel_id)
        for index, message in enumerate(messages):
            self.logger.info('Editing and deleting (%s/%s) on %s', index + 1, len(messages), self.channel_id)
            
            self.discord_api.edit_message(message['channel_id'], message['id'], random_word())
            self.discord_api.delete_message(message['channel_id'], message['id'])