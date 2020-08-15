from cleo import Command

from sanitize.common import load_yml
from sanitize.errors import ArgumentIsNotFound
from sanitize.plugins.discord.routines import DiscordRoutines

class DiscordCommand(Command):
    """
    Commands to sanitize a discord account.

    discord
        {--t|token=? : Must be set. It is used to authenticated into a particular account.}
        {--c|channel=? : If set, it will only clean that particular channel.}
        {--a|all : If set, it will clean all the channels found in a discord account.}
        {--f|file=? : Config file so users don't have to type everything.}
    """
    def handle(self):
        config_file = self.option('file')
        if config_file:
            config = load_yml(self.option('file')['discord'])
        else:
            config = {
                'token': self.option('token'),
                'channel': self.option('channel'),
                'all': self.option('all'),
            }

        self.execute(**config)

    def execute(self, token, channel, all):
        if not token:
            raise ArgumentIsNotFound('Token is not found')

        if channel:
            DiscordRoutines(token).sanitize_channel(channel)
        
        if all:
            DiscordRoutines(token).sanitize_account()
