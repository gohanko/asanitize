from cleo import Command

from sanitize.errors import ArgumentIsNotFound
from sanitize.plugins.discord.routines import DiscordRoutines

class DiscordCommand(Command):
    """
    Commands to sanitize a discord account.

    discord
        {--t|token= : Must be set. It is used to authenticated into a particular account.}
        {--c|channel=? : If set, it will only clean that particular channel.}
        {--a|all : If set, it will clean all the channels found in a discord account.}
    """
    def handle(self):
        token = self.option('token')
        if not token:
            raise ArgumentIsNotFound('token')

        channel_id = self.option('channel')
        if channel_id:
            DiscordRoutines(token).sanitize_channel(channel_id)
        
        if self.option('all'):
            DiscordRoutines(token).sanitize_account()
