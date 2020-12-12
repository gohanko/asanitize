from cleo import Command
from sanitize.common import load_config_from_file
from sanitize.discord.routine import DiscordRoutine

class DiscordCommand(Command):
    """
    Commands to sanitize a discord account.

    discord
        {token : Must be set. It is used to access a particular account to perform tasks.}
        {channel : Must be set. Values are either the channel id that you want to sanitize or the string 'all' to clean everything.}
        {file? : Set if you have a config file containing the authentication details. Please have a look at example.env.yml for example on how to create one.}
    """
    def handle(self):
        config_file = load_config_from_file(self.argument('file'), 'discord')
        if config_file:
            token = config_file.get('token')
            target = config_file.get('target')
        else:
            token = self.argument('token')
            target = self.argument('target')

        routine = DiscordRoutine(token) # check if token is good
        if target == 'all':
            routine.sanitize_account()
        else:
            routine.sanitize_channel(target)
