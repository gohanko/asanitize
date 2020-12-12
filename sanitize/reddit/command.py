from cleo import Command
from sanitize.reddit.routine import RedditRoutine

class RedditCommand(Command):
    """
    Commands to sanitize a reddit account.

    reddit
        {client-id : Must be set. Client ID used to authenticate.}
        {client-secret : Must be set. Client secret used to authenticate.}
        {username : Must be set. Username of the account.}
        {password : Must be set. Password of the account.}
        {two-factor? : Set if you have two factor authentication on your account.}
        {file? : Set if you have a config file containing the authentication details. Please have a look at example.env.yml for example on how to create one.}
    """
    def handle(self):
        config_file = load_config_from_file(self.argument('file'), 'reddit')
        if config_file:
            client_id = config_file.get('client-id')
            client_secret = config_file.get('client-secret')
            username = config_file.get('username')
            password = config_file.get('password')
            two_factor = config_file.get('two-factor')
        else:
            client_id = self.argument('client-id')
            client_secret = self.argument('client-secret')
            username = self.argument('username')
            password = self.argument('password')
            two_factor = self.argument('two-factor')

        routine = RedditRoutine(client_id, client_secret, username, password, two_factor)
        routine.sanitize_all()
