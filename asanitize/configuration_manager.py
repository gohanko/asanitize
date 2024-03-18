import sys
import os
import json
from dataclasses import dataclass, field

DEFAULT_CONFIGURATION_DIRECTORY = './asanitize.json'

@dataclass
class DiscordConfiguration(object):
    token: str = ''
    channels_to_sanitize: list[str] = field(default_factory=list)
    fastmode: bool = False

@dataclass
class RedditConfiguration(object):
    client_id: str = ''
    client_secret: str = ''
    username: str = ''
    password: str = ''


class ConfigurationManager(object):
    discord_config: DiscordConfiguration = DiscordConfiguration()
    reddit_config: RedditConfiguration = RedditConfiguration()

    def load_config(self, filename):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            raise Exception("Cannot load config file")
        else:
            self.discord_config = DiscordConfiguration(
                data.get('discord').get('token'),
                data.get('discord').get('channels_to_sanitize'),
                data.get('discord').get('fastmode'))

            self.reddit_config = RedditConfiguration(
                data.get('reddit').get('client_id'),
                data.get('reddit').get('client_secret'),
                data.get('reddit').get('username'),
                data.get('reddit').get('password'))

            return data

    def _save_config(self):
        config = {
            'discord': self.discord_config.__dict__,
            'reddit': self.reddit_config.__dict__
        }

        if not os.path.exists(DEFAULT_CONFIGURATION_DIRECTORY):
            new_file = open(DEFAULT_CONFIGURATION_DIRECTORY, 'w')
            json.dump(
                {'discord': self.discord_config.__dict__, 'reddit': self.reddit_config.__dict__},
                new_file,
                indent=4)
                
            new_file.close()

        with open(DEFAULT_CONFIGURATION_DIRECTORY, 'w') as file:
            json.dump(config, file, indent=4)

    def get_service_config(self, service):
        if service == 'discord':
            return self.discord_config

        if service == 'reddit':
            return self.reddit_config

    def set_service_config(self, service, **kwargs):
        if service == 'discord':
            self.discord_config.token = kwargs.get('token')
            self.discord_config.channels_to_sanitize = kwargs.get('channels_to_sanitize')
            self.discord_config.fastmode = kwargs.get('fastmode')

        if service == 'reddit':
            self.reddit_config.client_id = kwargs.get('client_id')
            self.reddit_config.client_secret = kwargs.get('client_secret')
            self.reddit_config.username = kwargs.get('username')
            self.reddit_config.password = kwargs.get('password')

        self._save_config()