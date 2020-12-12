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

        getattr(self, args.service)()

    def discord(self):
        parser = argparse.ArgumentParser(prog='sanitize.py discord', description='Command to sanitize a discord account.')
        parser.add_argument('token', help='Must be set. It is used to access a particular account to perform sanitization tasks.')
        parser.add_argument('channel', help='Must be set. Values are either the channel id that you want to sanitize or the string \'all\' to clean everything.')
        parser.add_argument('--file', help='Set if you have a config file containing the authentication details. Please have a look at example.env.yml for example on how to create one.')

        args = parser.parse_args(sys.argv[2:])
        if args.file:
            config_file = load_config_from_file(args.file, 'discord')
            token = config_file.get('token')
            channel = config_file.get('channel')
        else:
            token = args.token
            channel = args.channel

        routine = DiscordRoutine(token)
        if channel == 'all':
            routine.sanitize_account()
        else:
            routine.sanitize_channel(channel)

    def reddit(self):
        parser = argparse.ArgumentParser(prog='sanitize.py reddit', description='Command to sanitize a reddit account.')
        parser.add_argument('client_id', help='Must be set. Client ID used to authenticate.')
        parser.add_argument('client_secret', help='Must be set. Client secret used to authenticate.')
        parser.add_argument('username', help='Must be set. Username of the account.')
        parser.add_argument('password', help='Must be set. Password of the account.')
        parser.add_argument('two_factor', help='Set if you have two factor authentication on your account.')
        parser.add_argument('--file', help='Set if you have a config file containing the authentication details. Please have a look at example.env.yml for example on how to create one.')

        args = parser.parse_args(sys.argv[2:])
        if args.file:
            config_file = load_config_from_file(args.file, 'reddit')
            client_id = config_file.get('client-id')
            client_secret = config_file.get('client-secret')
            username = config_file.get('username')
            password = config_file.get('password')
            two_factor = config_file.get('two-factor')
        else:
            client_id = args.client_id
            client_secret = args.client_secret
            username = args.username
            password = args.password
            two_factor = args.two_factor

        routine = RedditRoutine(client_id, client_secret, username, password, two_factor)
        routine.sanitize_all()
