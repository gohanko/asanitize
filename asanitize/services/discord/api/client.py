from asanitize.services.discord.api import session, build_url
from asanitize.services.discord.api.data import DirectMessageChannelList, GuildList, User
from asanitize.services.discord.api.exceptions import AuthenticationTokenMissingError, ConnectionError

class Client(object):
    token = None
    current_user_info = None

    def __init__(self, token: str) -> None:
        self.token = token
        if not token:
            raise AuthenticationTokenMissingError('Missing discord authentication token')
        
        session.headers.update({'Authorization': token })

        if not self.is_connection_ok():
            raise ConnectionError('Connection error')

    def is_connection_ok(self) -> bool:
        status = session.get(build_url('users', '@me'))
        return status.status_code == 200

    def get_my_info(self) -> User:
        current_user_url = build_url('users', '@me')
        response = session.get(current_user_url).json()
        current_user = User(
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

        self.current_user_info = current_user
        return current_user

    def get_direct_message_channels(self) -> DirectMessageChannelList:
        direct_messages_url = build_url('users', '@me', 'channels')
        response = session.get(direct_messages_url).json()
        return DirectMessageChannelList(response)

    def get_guilds(self) -> GuildList:
        guilds_url = build_url('users', '@me', 'guilds')
        response = session.get(guilds_url).json()
        return GuildList(guild_list=response)
