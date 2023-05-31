from dataclasses import dataclass
from tqdm import tqdm
from time import sleep

from asanitize.data_structure.linked_list import LinkedList
from asanitize.services.discord.data.message import Message


@dataclass
class MessageList:
    messages: LinkedList

    sanitize_curr: int
    total_results: int

    def __init__(self, total_results: int = 0) -> None:
        self.messages = LinkedList()
        self.total_results = total_results

    def init_progress_bar(self):
        self.progress_bar = tqdm(total=self.total_results)

    def append(self, message_list: list):
        for message in message_list:
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
        for i in range(0, self.messages.count):
            message = self.messages.find(i)
            message.item.sanitize(is_fast_mode)
            self.progress_bar.update(1)
        
        self.messages = LinkedList()

    def __exit__(self):
        self.progress_bar.close()
