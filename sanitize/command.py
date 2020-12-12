from cleo import Application, Command
from sanitize.common import load_yml
from sanitize.services.discord import DiscordRoutine
from sanitize.services.reddit import RedditRoutine

class DiscordCommand(Command):
    """
    Commands to sanitize a discord account.

    discord
        {--a|auth-token=? : Must be set. It is used to authenticated into a particular account.}
        {--t|target=? : Must be set. Values are either the channel id that you want to sanitize or the string 'all' to clean everything.}
        {--f|file=? : Config file so users don't have to type everything.}
    """
    def handle(self):
        config_file = self.option('file')
        if config_file:
            config = load_yml(config_file)['discord']
            token = config['auth-token']
            target = config['target']
        else:
            token = self.option('auth-token')
            target = self.option('target')

        if not token:
            print('Token is not found!')
            return

        if not target:
            print('Target is not found!')
            return

        routine = DiscordRoutine(token)
        if target == 'all':
            routine.sanitize_account()
        else:
            routine.sanitize_channel(target)

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

        routine = RedditRoutine(client_id, client_secret, username, password, two_factor)
        routine.sanitize_all()

def handle_command():
    cleo_commands = [DiscordCommand(), RedditCommand()]

    application = Application()
    for cleo_command in cleo_commands:
        application.add(cleo_command)

    application.run()
