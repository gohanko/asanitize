import time
from dataclasses import dataclass, field

from asanitize.common import random_word
from asanitize.services.discord import build_url, session
from asanitize.services.discord.data.user import User

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
