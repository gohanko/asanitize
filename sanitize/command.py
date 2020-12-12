import sys
import argparse
from sanitize.common import load_config_from_file
from sanitize.services.discord import DiscordRoutine
from sanitize.services.reddit import RedditRoutine

activated_services = ['discord', 'reddit']

# https://chase-seibert.github.io/blog/2014/03/21/python-multilevel-argparse.html
class Command:
    def __init__(self):
        parser = argparse.ArgumentParser(prog='sanitize.py', description='Software to sanitize your online accounts.')
        parser.add_argument('service', help='Select the service to be sanitize. Currently supports \'discord\' and \'reddit\'.')
        
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.service) and args.service in activated_services:
            print('Unrecognized service')
            parser.print_help()
            exit(1)

        getattr(self, args.service)(sys.argv[2:])

    def _handle_discord_args(self, args):
        if args.file:
            config = load_config_from_file(args.file, 'discord')
            token = config.get('token')
            channel = config.get('channel')
        else:
            token = args.token
            channel = args.channel

        routine = DiscordRoutine(token)
        if channel == 'all':
            routine.sanitize_account()
        else:
            routine.sanitize_channel(channel)

    def discord(self, args):
        parser = argparse.ArgumentParser(prog='sanitize.py discord', description='Command to sanitize a discord account.')
        parser.add_argument('token', help='Must be set. It is used to access a particular account to perform sanitization tasks.')
        parser.add_argument('channel', help='Must be set. Values are either the channel id that you want to sanitize or the string \'all\' to clean everything.')
        parser.add_argument('--file', help='Set if you have a config file containing the authentication details. Please have a look at example.env.yml for example on how to create one.')

        parsed_arguments = parser.parse_args(args)
        self._handle_discord_args(parsed_arguments)

    def _handle_reddit_args(self, args):
        if args.file:
            config = load_config_from_file(args.file, 'reddit')
            client_id = config.get('client-id')
            client_secret = config.get('client-secret')
            username = config.get('username')
            password = config.get('password')
            two_factor = config.get('two-factor')
        else:
            client_id = args.client_id
            client_secret = args.client_secret
            username = args.username
            password = args.password
            two_factor = args.two_factor

        routine = RedditRoutine(client_id, client_secret, username, password, two_factor)
        routine.sanitize_all()

    def reddit(self, args):
        parser = argparse.ArgumentParser(prog='sanitize.py reddit', description='Command to sanitize a reddit account.')
        parser.add_argument('client_id', help='Must be set. Client ID used to authenticate.')
        parser.add_argument('client_secret', help='Must be set. Client secret used to authenticate.')
        parser.add_argument('username', help='Must be set. Username of the account.')
        parser.add_argument('password', help='Must be set. Password of the account.')
        parser.add_argument('two_factor', help='Set if you have two factor authentication on your account.')
        parser.add_argument('--file', help='Set if you have a config file containing the authentication details. Please have a look at example.env.yml for example on how to create one.')

        parsed_arguments = parser.parse_args(args)
        self._handle_reddit_args(parsed_arguments)
