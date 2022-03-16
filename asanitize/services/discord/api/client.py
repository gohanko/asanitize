from . import session, build_url
from .data import DirectMessageChannelList, GuildList, MessageList

class Client(object):
    def __init__(self, token: str) -> None:
        self.token = token
        if not token:
            raise AuthenticationTokenMissingError("Missing discord authentication token")
        
        session.headers.update({'Authorization': DISCORD_AUTHENTICATION_TOKEN })

    def is_connection_ok(self) -> bool:
        status = session.get(build_url('users', '@me'))
        return status.status_code == 200

    def get_current_user_info(self) -> User:
        current_user_url = self.build('users', '@me')
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
            nsfw_allowed=response.get('nsfw_allowed'),
            mfa_enabled=response.get('mfa_enabled'),
            email=response.get('email'),
            verified=response.get('verified'),
            phone=response.get('phone'),
        )

        return current_user

    def get_direct_messages(self) -> DirectMessageList:
        direct_messages_url = build_url('users', '@me', 'channels')
        response = session.get(direct_messages_url).json()
        return DirectMessageChannelList(response)

    def get_guilds(self) -> GuildList:
        guilds_url = build_url('users', '@me', 'guilds')
        response = session.get(guilds_url, headers=self.headers).json()
        return GuildList(response)
