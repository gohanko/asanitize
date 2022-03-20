import time
from dataclasses import dataclass, field
from asanitize.data_structure.linked_list import LinkedList
from asanitize.services.discord.api import session, build_url
from asanitize.common import random_word

@dataclass
class User:
    id: str = ''
    username: str = ''
    avatar: str = ''
    discriminator: str = ''
    public_flags: int = 0
    flags: int = 0
    banner: str = ''
    banner_color: str = ''
    accent_color: str = ''
    bio: str = ''
    locale: str = ''
    nsfw_enabled: bool = False
    mfa_enabled: bool = False
    email: str = ''
    verified: bool = False
    phone: str = ''

@dataclass
class RoleTag:
    bot_id: str = ''

@dataclass
class Role:
    id: str = ''
    name: str = ''
    permissions: int = 0
    position: int = 0
    color: int = 0
    hoist: bool = False
    managed: bool = False
    mentionable: bool = False
    icon: str = ''
    unicode_emoji: str = ''
    tags: list[RoleTag] = field(default_factory=list)
    permissions_new: str = ''

@dataclass
class Emoji:
    name: str = ''
    roles: list[Role] = field(default_factory=list)
    id: str = ''
    require_colons: bool = False
    managed: bool = False
    animated: bool = False
    available: bool = False

@dataclass
class Sticker:
    id: str = ''
    name: str = ''
    tags: str = ''
    type: int = 0
    format_type: int = 0
    description: str = ''
    asset: str = ''
    available: bool = False
    guild_id: str = ''

@dataclass
class Message:
    id: str = ''
    type: int = 0
    content: str = ''
    channel_id: str = ''
    author: User = None
    attachments: list = field(default_factory=list)
    embeds: list = field(default_factory=list)
    mentions: list = field(default_factory=list)
    mention_roles: list = field(default_factory=list)
    pinned: bool = False
    mention_everyone: bool = False
    tts: bool = False
    timestamp: str = '' # todo: maybe change to actual date time format?
    edited_timestamp: str = ''
    flags: int = 0
    components: list = field(default_factory=list)
    hit: bool = False

    def edit(self, new_content: str) -> None:
        edit_message_url = build_url('channels', self.channel_id, 'messages', self.id)
        response = session.patch(
            edit_message_url, 
            headers={'Content-Type': 'application/json'}, 
            json={'content': new_content}
        )

        if response.status_code == 200:
            self.content = new_content

        if response.status_code == 429:
            sleep_interval = int(response.headers.get('retry-after')) / 1000
            time.sleep(sleep_interval)
            self.edit(new_content)

    # Can only delete it from discord servers but not itself from out list.
    def delete(self):
        delete_message_url = build_url('channels', self.channel_id, 'messages', self.id)
        response = session.delete(delete_message_url)

        if response.status_code == 429:
            sleep_interval = int(response.headers.get('retry-after')) / 1000
            time.sleep(sleep_interval)
            self.delete()

    def sanitize(self, is_fast_mode: bool) -> None:
        if not is_fast_mode:
            self.edit(random_word())

        self.delete()

@dataclass
class MessageList:
    messages: LinkedList

    def __init__(self, message_list: dict) -> None:
        self.messages = LinkedList()

        for message in message_list.get('messages'):
            self.messages.append(Message(
                id=message[0].get('id'),
                type=message[0].get('type'),
                content=message[0].get('content'),
                channel_id=message[0].get('channel_id'),
                author=message[0].get('author'),
                attachments=message[0].get('attachments'),
                embeds=message[0].get('embeds'),
                mentions=message[0].get('mentions'),
                mention_roles=message[0].get('mention_roles'),
                pinned=message[0].get('pinned'),
                mention_everyone=message[0].get('mention_everyone'),
                tts=message[0].get('tts'),
                timestamp=message[0].get('timestamp'),
                edited_timestamp=message[0].get('edited_timestamp'),
                flags=message[0].get('flags'),
                components=message[0].get('components'),
                hit=message[0].get('hit'),
            ))

    def sanitize_all(self, is_fast_mode: bool) -> None:
        for i in range(self.messages.count):
            print('    Sanitizing ({}/{})'.format(i + 1, self.messages.count))
            message = self.messages.find(i)
            message.item.sanitize(is_fast_mode)

@dataclass
class BaseChannel:
    id: str = ''

    def _get_search_url(self, author_id: str, offset: str) -> MessageList:
        pass

    def search(self, author_id: str, offset: str) -> MessageList:
        search_url = self._get_search_url(author_id, offset)
        response = session.get(search_url).json()
        return MessageList(response)

    def sanitize(self, author_id: str, is_fast_mode: bool) -> None:
        message_list = self.search(author_id, 0)
        if message_list.messages.count < 1:
            print('    No messages found! Skipping...')

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
        response = session.get(guild_info_url).json()

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
