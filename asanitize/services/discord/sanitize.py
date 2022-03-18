import time
from asanitize.services.discord.api.client import Client

def sanitize(token, channel_id, author_id=None, is_fast_mode=False):
    print('\n')
    start_time = time.perf_counter()

    client = Client(token)
    current_user_info = client.get_my_info()
    guild_list = client.get_guilds()
    direct_message_channel_list = client.get_direct_message_channels()

    if author_id is None:
        author_id = current_user_info.id

    if channel_id == 'all':
        guild_list.sanitize_all(author_id=author_id, is_fast_mode=is_fast_mode)
        direct_message_channel_list.sanitize_all(author_id=author_id, is_fast_mode=is_fast_mode)
    else:
        if guild_list.is_exist(channel_id):
            guild_list.sanitize(author_id=author_id, channel_id=channel_id, is_fast_mode=is_fast_mode)

        if direct_message_channel_list.is_exist(channel_id):
            direct_message_channel_list.sanitize(author_id=author_id, channel_id=channel_id, is_fast_mode=is_fast_mode)

    end_time = time.perf_counter()

    print('\n********************************')
    print(f'Start time     : {start_time}')
    print(f'End time       : {end_time}')
    print(f'Execution time : {end_time - start_time:0.6f}s')
    print('********************************\n')
