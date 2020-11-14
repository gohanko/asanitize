from cleo import Application, Command
from sanitize.common import load_yml
from sanitize.errors import ArgumentIsNotFound
from sanitize.services.discord import Routine
from sanitize.services.reddit import Routine

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

class RedditCommand(Command):
    """
    Commands to sanitize a reddit account.

    reddit
        {--c|client-id=? : Must be set. Client ID used to authenticate.}
        {--s|client-secret=? : Must be set. Client secret used to authenticate.}
        {--u|username=? : Must be set. Username of the account.}
        {--p|password=? : Must be set. Password of the account.}
        {--t|two-factor=? : Set if you have two factor authentication on your account.}
    """
    def handle(self):
        client_id = self.option('client-id')
        client_secret = self.option('client-secret')
        username = self.option('username')
        password = self.option('password')
        two_factor = self.option('two-factor')

        routine = Routine(client_id, client_secret, username, password, two_factor)
        routine.sanitize_all()

def handle_command():
    cleo_commands = [DiscordCommand(), RedditCommand()]

    application = Application()
    for cleo_command in cleo_commands:
        application.add(cleo_command)

    application.run()
