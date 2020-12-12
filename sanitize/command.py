import sys
import argparse
from sanitize.common import load_config_from_file
from sanitize.services.discord import DiscordRoutine
from sanitize.services.reddit import RedditRoutine

# https://chase-seibert.github.io/blog/2014/03/21/python-multilevel-argparse.html
class Command:
    def __init__(self):
        parser = argparse.ArgumentParser(prog='sanitize.py', description='Software to sanitize your online accounts.')
        parser.add_argument('service', help='Select the service to be sanitize. Currently supports \'discord\' and \'reddit\'.')
        
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.service):
            print('Unrecognized service')
            parser.print_help()
            exit(1)

        getattr(self, args.service)(sys.argv[2:])

    def discord(self, args):
        parser = argparse.ArgumentParser(prog='sanitize.py discord', description='Command to sanitize a discord account.')
        parser.add_argument('token', help='Must be set. It is used to access a particular account to perform sanitization tasks.')
        parser.add_argument('channel', help='Must be set. Values are either the channel id that you want to sanitize or the string \'all\' to clean everything.')
        parser.add_argument('--file', help='Set if you have a config file containing the authentication details. Please have a look at example.env.yml for example on how to create one.')

        parsed_arguments = parser.parse_args(args)
        if args.file:
            config = load_config_from_file(args.file, 'discord')
        else:
            config = { 'token': args.token, 'channel': args.channel }

        routine = DiscordRoutine(config.get('token'))
        if config.get('channel') == 'all':
            routine.sanitize_account()
        else:
            routine.sanitize_channel(config.get('channel'))

    def reddit(self, args):
        parser = argparse.ArgumentParser(prog='sanitize.py reddit', description='Command to sanitize a reddit account.')
        parser.add_argument('client_id', help='Must be set. Client ID used to authenticate.')
        parser.add_argument('client_secret', help='Must be set. Client secret used to authenticate.')
        parser.add_argument('username', help='Must be set. Username of the account.')
        parser.add_argument('password', help='Must be set. Password of the account.')
        parser.add_argument('two_factor', help='Set if you have two factor authentication on your account.')
        parser.add_argument('--file', help='Set if you have a config file containing the authentication details. Please have a look at example.env.yml for example on how to create one.')

        parsed_arguments = parser.parse_args(args)
        if args.file:
            config = load_config_from_file(args.file, 'reddit')
        else:
            config = {
                'client_id': args.client_id,
                'client_secret': args.client_secret,
                'username': args.username,
                'password': args.password,
                'two_factor': args.two_factor
            }

        routine = RedditRoutine(
            config.get('client_id'),
            config.get('client_secret'),
            config.get('username'),
            config.get('password'),
            config.get('two_factor'),
        )
        routine.sanitize_all()
