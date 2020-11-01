from cleo import Command

from sanitize.plugins.reddit.routine import Routine

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
