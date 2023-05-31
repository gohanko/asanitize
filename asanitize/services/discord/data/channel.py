from dataclasses import dataclass, field
import math

from asanitize.services.discord import build_url
from asanitize.services.discord.data.http_middleware import HTTPMiddleware
from asanitize.services.discord.data.message_list import MessageList
from asanitize.services.discord.data.message import Emoji, Sticker, Role, RoleTag
from asanitize.services.discord.data.user import User


@dataclass
class BaseChannel(HTTPMiddleware):
    id: str = ''

    def _get_search_url(self, author_id: str, offset: str) -> MessageList:
        pass

    def search(self, author_id: str, offset: str) -> MessageList:
        search_url = self._get_search_url(author_id, offset)
        response = self.get(search_url)
        return response.json().get('messages')

    def sanitize(self, author_id: str, is_fast_mode: bool) -> None:
        total_results = self.get(self._get_search_url(author_id, 0)).json().get('total_results')

        message_list = MessageList(total_results)
        aa = math.ceil(total_results / 25)
        for i in range(0, math.ceil(total_results / 25)):
            message_list.append(self.search(author_id, i * 25))
            message_list.sanitize_all(is_fast_mode)



@dataclass
class Guild(BaseChannel):
    name: str = ''
    icon: str = ''
    description: str = ''
    splash: str = ''
    discovery_splash: str = ''
    features: list[str] = field(default_factory=list)
    emojis: list[Emoji] = field(default_factory=list)
    stickers: list[Sticker] = field(default_factory=list)
    banner: bool = False
    owner: bool = False
    owner_id: str = ''
    application_id: str = ''
    region: str = ''
    afk_channel_id: str = ''
    afk_timeout: int = 0
    system_channel_id: str = ''
    widget_enabled: bool = False
    widget_channel_id: str = ''
    verification_level: int = 0
    roles: list[Role] = field(default_factory=list)
    default_message_notifications: int = 0
    mfa_level: int = 0
    explicit_content_filters: int = 0
    max_presences: int = 0
    max_members: int = 0
    max_video_channel_users: int = 0
    vanity_url_code: str = ''
    premium_tier: int = 0
    premium_subscription_count: int = 0
    system_channel_flags: int = 0
    preferred_locale: str = ''
    rules_channel_id: str = ''
    public_updates_channel_id: str = ''
    hub_type: str = ''
    premium_progress_bar_enabled: bool = False
    nsfw: bool = False
    nsfw_level: int = 0
    embed_enabled: bool = False
    embed_channel_id: str = ''

    def info(self):
        guild_info_url = build_url('channels', self.id)
        response = self.get(guild_info_url).json()

        emojis = []
        for emoji in response.get('emojis'):
            emoji_roles = []
            for emoji_role in emoji.get('roles'):
                emoji_role.append(Role(
                    id=emoji_role.get('id'),
                    name=emoji_role.get('name'),
                    permissions=emoji_role.get('permissions'),
                    color=emoji_role.get('color'),
                    hoist=emoji_role.get('hoist'),
                    managed=emoji_role.get('managed'),
                    mentionable=emoji_role.get('mentionable'),
                    icon=emoji_role.get('icon'),
                    unicode_emoji=emoji_role.get('unicode_emoji'),
                    tags=[RoleTag(bot_id=tag.get('bot_id')) for tag in emoji_role.get('tags')],
                    permissions_new=emoji_role.get('permissions_new'),
                ))

            emojis.append(Emoji(
                name=emoji.get('name'),
                roles=emoji_roles,
                id=emoji.get('id'),
                require_colons=emoji.get('require_colons'),
                managed=emoji.get('managed'),
                animated=emoji.get('animated'),
                available=emoji.get('available'),
            ))

        stickers = []
        for sticker in response.get('stickers'):
            stickers.append(Sticker(
                id=sticker.get('id'),
                name=sticker.get('name'),
                tags=sticker.get('tags'),
                type=sticker.get('type'),
                format_type=sticker.get('format_type'),
                description=sticker.get('description'),
                asset=sticker.get('asset'),
                available=sticker.get('available'),
                guild_id=sticker.get('guild_id'),
            ))

        roles = []
        for role in response.get('roles'):
            roles.append(Role(
                id=role.get('id'),
                name=role.get('name'),
                permissions=role.get('permissions'),
                position=role.get('position'),
                color=role.get('color'),
                hoist=role.get('hoist'),
                managed=role.get('managed'),
                mentionable=role.get('mentionable'),
                icon=role.get('icon'),
                unicode_emoji=role.get('unicode_emoji'),
                tags=[RoleTag(bot_id=tag.get('bot_id')) for tag in role.get('tags')],
                permissions_new=role.get('permissions_new'),
            ))

        self.__init__(
            id=response.get('id'),
            name=response.get('name'),
            icon=response.get('icon'),
            description=response.get('description'),
            splash=response.get('splash'),
            discovery_splash=response.get('discovery_splash'),
            features=response.get('features'),
            emojis=emojis,
            stickers=stickers,
            banner=response.get('banner'),
            owner_id=response.get('owner_id'),
            application_id=response.get('application_id'),
            region=response.get('region'),
            afk_channel_id=response.get('afk_channel_id'),
            afk_timeout=response.get('afk_timeout'),
            system_channel_id=response.get('system_channel_id'),
            widget_enabled=response.get('widget_enabled'),
            widget_channel_id=response.get('widget_channel_id'),
            verification_level=response.get('verification_level'),
            roles=roles,
            default_message_notifications=response.get('default_message_notifications'),
            mfa_level=response.get('mfa_level'),
            explicit_content_filters=response.get('explicit_content_filters'),
            max_presences=response.get('max_presences'),
            max_members=response.get('max_members'),
            max_video_channel_users=response.get('max_video_channel_users'),
            vanity_url_code=response.get('vanity_url_code'),
            premium_tier=response.get('premium_tier'),
            premium_subscription_count=response.get('premium_subscription_count'),
            system_channel_flags=response.get('system_channel_flags'),
            preferred_locale=response.get('preferred_locale'),
            rules_channel_id=response.get('rules_channel_id'),
            public_updates_channel_id=response.get('rules_channel_id'),
            hub_type=response.get('hub_type'),
            premium_progress_bar_enabled=response.get('premium_progress_bar_enabled'),
            nsfw=response.get('nsfw'),
            nsfw_level=response.get('nsfw_level'),
            embed_enabled=response.get('embed_enabled'),
            embed_channel_id=response.get('embed_channel_id'),
        )

    def _get_search_url(self, author_id: str, offset: str) -> MessageList:
        search_url = build_url(
            'guilds', 
            self.id, 
            'messages', 
            'search?author_id={}&include_nsfw=true'.format(author_id)
        )

        if offset:
            search_url = '{}&offset={}'.format(search_url, offset)
        
        return search_url


@dataclass
class DirectMessageChannel(BaseChannel):
    type: int = 0
    last_message_id: str = ''
    recipients: list[User] = field(default_factory=list)

    def _get_search_url(self, author_id: str, offset: str) -> MessageList:
        search_url = build_url(
            'channels', 
            self.id, 
            'messages', 
            'search?author_id={}&include_nsfw=true'.format(author_id)
        )

        if offset:
            search_url = '{}&offset={}'.format(search_url, offset)

        return search_url
