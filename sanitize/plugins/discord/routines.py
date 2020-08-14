from sanitize.plugins.discord.api import DiscordAPI
from sanitize.plugins.discord.channel import Channel

class DiscordRoutines:
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