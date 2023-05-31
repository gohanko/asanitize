import time
from asanitize.services.discord.client import Client


def sanitize(token: str, channels_to_sanitize: list, author_id:str = None, is_fast_mode: bool = False):
    start_time = time.perf_counter()

    client = Client(token)
    current_user_info = client.current_user_info
    guild_list = client.get_guilds()
    direct_message_channel_list = client.get_direct_message_channels()

    if author_id is None:
        author_id = current_user_info.id

    if channels_to_sanitize == []:
        guild_list.sanitize_all(author_id=author_id, is_fast_mode=is_fast_mode)
        direct_message_channel_list.sanitize_all(author_id=author_id, is_fast_mode=is_fast_mode)
    else:
        for channel_id in channels_to_sanitize:
            if guild_list.is_exist(channel_id):
                guild_list.sanitize(author_id=author_id, channel_id=channel_id, is_fast_mode=is_fast_mode)

            if direct_message_channel_list.is_exist(channel_id):
                direct_message_channel_list.sanitize(author_id=author_id, channel_id=channel_id, is_fast_mode=is_fast_mode)

    end_time = time.perf_counter()

    print(f'\nStart Time: {start_time} | End Time: {end_time} | Execution Time: {end_time - start_time:0.6f}s')
