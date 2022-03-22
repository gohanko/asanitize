from dataclasses import dataclass, field

from asanitize.services.discord.data.channel import Guild, DirectMessageChannel
from asanitize.services.discord.data.user import User


@dataclass
class BaseChannelList(object):
    def is_exist(self, channel_id):
        for channel in self.channels:
            if channel.id == channel_id:
                return True
        return False

    def _get_info_text(self, channel) -> str:
        try:
            recipients = ', '.join(['{}#{}'.format(recipient.username, recipient.discriminator) for recipient in channel.recipients])
        except AttributeError:
            recipients = None
        
        if recipients:
            return 'Sanitizing chat with {} :'.format(recipients)
        else:
            return 'Sanitizing guild {} :'.format(channel.name)

    def sanitize(self, author_id: str, channel_id: str, is_fast_mode: bool) -> None:        
        for channel in self.channels:
            if channel.id == channel_id:
                print(self._get_info_text(channel))
                channel.sanitize(author_id, is_fast_mode)

    def sanitize_all(self, author_id: str, is_fast_mode: bool) -> None:
        for channel in self.channels:
            print(self._get_info_text(channel))
            channel.sanitize(author_id, is_fast_mode)


@dataclass
class GuildList(BaseChannelList):
    channels: list[Guild] = field(default_factory=list)

    def __init__(self, guild_list: list) -> None:
        self.channels = []
        for channel in guild_list:
            self.channels.append(Guild(
                id=channel.get('id'),
                name=channel.get('name'),
                icon=channel.get('icon'),
                owner=channel.get('owner'),
                features=channel.get('features'),
            ))


@dataclass
class DirectMessageChannelList(BaseChannelList):
    channels: list = field(default_factory=list)

    def __init__(self, direct_message_list: list) -> None:
        self.channels = []
        for channel in direct_message_list:
            recipients = []
            for recipient in channel.get('recipients'):
                recipients.append(User(
                    id=recipient.get('id'),
                    username=recipient.get('username'),
                    avatar=recipient.get('avatar'),
                    discriminator=recipient.get('discriminator'),
                    public_flags=recipient.get('public_flags'),
                ))

            self.channels.append(DirectMessageChannel(
                id=channel.get('id'),
                type=channel.get('type'),
                last_message_id=channel.get('last_message_id'),
                recipients=recipients
            ))
