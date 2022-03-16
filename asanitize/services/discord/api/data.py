import time
from dataclasses import dataclass
from . import session, build_url

@dataclass
class User:
    id: str
    username: str
    avatar: str
    discriminator: str
    public_flags: int
    flags: int
    banner: str
    banner_color: str
    accent_color: str
    bio: str
    locale: str
    nsfw_enabled: bool
    mfa_enabled: bool
    email: str
    verified: bool
    phone: str

@dataclass
class RoleTag:
    bot_id: str

@dataclass
class Role:
    id: str
    name: str
    permissions: int
    position: int
    color: int
    hoist: bool
    managed: bool
    mentionable: bool
    icon: str
    unicode_emoji: str
    tags: list[RoleTag]
    permissions_new: str

@dataclass
class Emoji:
    name: str
    roles: list[Role]
    id: str
    require_colons: bool
    managed: bool
    animated: bool
    available: bool

@dataclass
class Sticker:
    id: str
    name: str
    tags: str
    type: int
    format_type: int
    description: str
    asset: str
    available: bool
    guild_id: str

@dataclass
class Guild:
    id: str
    name: str
    icon: str
    description: str
    splash: str
    discovery_splash: str
    features: list[str]
    emojis: list[Emoji]
    stickers: list[Sticker]
    banner: bool
    owner: bool
    owner_id: str
    application_id: str
    region: str
    afk_channel_id: str
    afk_timeout: int
    system_channel_id: str
    widget_enabled: bool
    widget_channel_id: null
    verification_level: int
    roles: list[Role]
    default_message_notifications: int
    mfa_level: int
    explicit_content_filters: int
    max_presences: int
    max_members: int
    max_video_channel_users: int
    vanity_url_code: str
    premium_tier: int
    premium_subscription_count: int
    system_channel_flags: int
    preferred_locale: str
    rules_channel_id: str
    public_updates_channel_id: str
    hub_type: str
    premium_progress_bar_enabled: bool
    nsfw: bool
    nsfw_level: int
    embed_enabled: bool
    embed_channel_id: str

    def info(self):
        guild_info_url = build_url('channels', self.id)
        response = session.get(guild_info_url).json()

        emojis = []
        for emoji in response.get('emojis')
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
        for sticker in response.get('stickers')
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

    def search(self, author_id: str, offset: str) -> MessageList:
        search_url = build_url(
            'guilds', 
            self.id, 
            'messages', 
            'search?author_id{}&include_nsfw=true'.format(author_id)
        )

        if offset:
            search_url = '{}&offset={}'.format(search_url, offset)

        response = session.get(search_url).json()
        return MessageList(response)

@dataclass
class GuildList:
    guilds: list

    def __init__(self, guild_list: list) -> None:
        for guild in guild_list:
            self.guilds.append(Guild(
                id=guild.get('id'),
                name=guild.get('name'),
                icon=guild.get('icon'),
                owner=guild.get('owner'),
                features=guild.get('features'),
            ))

@dataclass
class Channel:
    id: str
    type: int
    last_message_id: str
    recipients: list[User]

    def search(self, author_id: str, offset: str) -> MessageList:
        search_url = build_url(
            'channels', 
            self.id, 
            'messages', 
            'search?author_id{}&include_nsfw=true'.format(author_id)
        )

        if offset:
            search_url = '{}&offset={}'.format(search_url, offset)

        response = session.get(search_url).json()
        return MessageList(response)

    def sanitize(self, author_id: str) -> None:
        messages = self.search(author_id, 0)



@dataclass
class DirectMessageChannelList:
    direct_message_channels: list

    def __init__(self, direct_message_list: list) -> None:
        for direct_message in direct_message_list:
            recipients = []
            for recipient in direct_message.get('recipients'):
                recipients.append(User(
                    id=recipient.get('id'),
                    username=recipient.get('username'),
                    avatar=recipient.get('avatar'),
                    discriminator=recipient.get('discriminator'),
                    public_flags=recipient.get('public_flags'),
                ))
            
            direct_message_channel = Channel(
                id=direct_message.get('id'),
                type=direct_message.get('type'),
                last_message_id=direct_message.get('last_message_id'),
                recipients=recipients
            )

            self.direct_message_channels.append(direct_message_channel)

@dataclass
class Message:
    id: str
    type: int
    content: str
    channel_id: str
    author: User
    attachments: list
    embeds: list
    mentions: list
    mention_roles: list
    pinned: bool
    mention_everyone: bool
    tts: bool
    timestamp: str # todo: maybe change to actual date time format?
    edited_timestamp: str
    flags: int
    components: list
    hit: bool

    def edit(self, new_content):
        edit_message_url = build_url('channels', self.channel_id, 'messages', self.id)
        response = session.patch(
            edit_message_url, 
            headers={'Content-Type': 'application/json'}, 
            json={'content': new_content}
        )

        if response.status_code == 200:
            content = new_content

        if response.status_code == 429:
            sleep_interval = int(response.headers.get('retry-after')) / 1000
            time.sleep(sleep_interval)
            self.edit(new_content)

    # Can only delete it from discord servers but not itself from out list.
    def delete(self):
        delete_message_url = build_url('channels', channel_id, 'messages', self.id)
        response = session.delete(delete_message_url)

        if response.status_code == 429:
            sleep_interval = int(response.headers.get('retry-after')) / 1000
            time.sleep(sleep_interval)
            delete()

class MessageList:
    messages: list

    def __init__(self, message_list):
        for message in message_list.get('messages'):
            messages.append(Message(
                id=message.get('id'),
                type=message.get('type'),
                content=message.get('content'),
                channel_id=message.get('channel_id'),
                author=message.get('author'),
                attachments=message.get('attachments'),
                embeds=message.get('embeds'),
                mentions=message.get('mentions'),
                mention_roles=message.get('mention_roles'),
                pinned=message.get('pinned'),
                mention_everyone=message.get('mention_everyone'),
                tts=message.get('tts'),
                timestamp=message.get('timestamp'),
                edited_timestamp=message.get('edited_timestamp'),
                flags=message.get('flags'),
                components=message.get('components'),
                hit=message.get('hit'),
            ))

    def delete_all(self):
        for message in messages:
            message.delete()

