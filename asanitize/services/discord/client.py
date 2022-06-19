from asanitize.services.discord import session, build_url
from asanitize.services.discord.data.http_middleware import HTTPMiddleware
from asanitize.services.discord.data.channel_list import DirectMessageChannelList, GuildList, User
from asanitize.services.discord.exceptions import AuthenticationTokenMissingError, ConnectionError


class Client(HTTPMiddleware):
    token = None
    current_user_info = None

    def __init__(self, token: str) -> None:
        self.token = token
        if not token:
            raise AuthenticationTokenMissingError('Missing discord authentication token')
        
        session.headers.update({'Authorization': token })

        response = self.get(build_url('users', '@me'))
        if response.status_code != 200:
            raise ConnectionError('Connection error')

        response = response.json()
        self.current_user_info = User(
            id=response.get('id'),
            username=response.get('username'),
            avatar=response.get('avatar'),
            discriminator=response.get('discriminator'),
            public_flags=response.get('public_flags'),
            flags=response.get('flags'),
            banner=response.get('banner'),
            banner_color=response.get('banner_color'),
            accent_color=response.get('accent_color'),
            bio=response.get('bio'),
            locale=response.get('locale'),
            nsfw_enabled=response.get('nsfw_enabled'),
            mfa_enabled=response.get('mfa_enabled'),
            email=response.get('email'),
            verified=response.get('verified'),
            phone=response.get('phone'),
        )

    def get_direct_message_channels(self) -> DirectMessageChannelList:
        direct_messages_url = build_url('users', '@me', 'channels')
        response = self.get(direct_messages_url).json()
        return DirectMessageChannelList(response)

    def get_guilds(self) -> GuildList:
        guilds_url = build_url('users', '@me', 'guilds')
        response = self.get(guilds_url).json()
        return GuildList(guild_list=response)
