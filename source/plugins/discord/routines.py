from .api import DiscordAPI

class DiscordRoutines(object):
    def __init__(self, authorization_token):
        self.discord_api = DiscordAPI(authorization_token)
        self.user_id = self.discord_api.get_current_user_id()
        self.cleanse_messages()

    def filter_messages_by_author(self, messages, author_id):
        filtered_messages = []
        for message in messages:
            if message['author']['id'] == author_id and message not in filtered_messages:
                filtered_messages.push(message)

        return filtered_messages

    def delete_all_current_users_message_in_dm(self, channel_id, author_id):
        messages = self.discord_api.search_dm(channel_id, author_id)
        for message in messages:
            self.discord_api.delete_message(message['id'])
    
    def delete_all_current_users_message_in_guild(self, channel_id, author_id):
        messages = self.discord_api.search_guild(channel_id, author_id)
        for message in messages:
            self.discord_api.delete_message(message['id'])

    def cleanse_messages(self):
        dms = self.discord_api.get_user_dms(self.user_id)
        for dm in dms:
            self.delete_all_current_users_message_in_dm(dm['id'], self.author_id)

        guilds = self.discord_api.get_user_guilds(self.user_id)
        for guild in guilds:
            self.delete_all_current_users_message_in_guild(guild['id'], self.author_id)