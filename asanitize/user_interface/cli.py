import sys
import argparse
from asanitize.common import load_config_from_file
from asanitize.services.discord.sanitize import sanitize
from asanitize.services.reddit.reddit import RedditRoutine

# https://chase-seibert.github.io/blog/2014/03/21/python-multilevel-argparse.html
class CommandLineInterface:
    def __init__(self):
        parser = argparse.ArgumentParser(prog='asanitize.py', description='Software to sanitize your online accounts.')
        parser.add_argument('service', help='Select the service to be sanitize. Currently supports \'discord\' and \'reddit\'.')
        
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.service):
            print('Unrecognized service')
            parser.print_help()
            exit(1)

        getattr(self, args.service)(sys.argv[2:])

    def discord(self, args):
        parser = argparse.ArgumentParser(prog='asanitize.py discord', description='Command to sanitize a discord account.')
        parser.add_argument('token', help='Must be set. It is used to access a particular account to perform sanitization tasks.')
        parser.add_argument('channel', help='Must be set. Values are either the channel id that you want to sanitize or the string \'all\' to clean everything.')
        parser.add_argument('--file', help='Set if you have a config file containing the authentication details. Please have a look at example.env.yml for example on how to create one.')
        parser.add_argument('--fastmode', help='If this is true, it will just delete message instead of editing and deleting. False by default.', action=argparse.BooleanOptionalAction)

        parsed_arguments = parser.parse_args(args)
        if parsed_arguments.file is not None:
            config = load_config_from_file(parsed_arguments.file, 'discord')
        else:
            config = { 'token': parsed_arguments.token, 'channel': parsed_arguments.channel, 'fastmode': parsed_arguments.fastmode }

        sanitize(config.get('token'), config.get('channel'), None, config.get('fastmode'))
      
    def reddit(self, args):
        parser = argparse.ArgumentParser(prog='asanitize.py reddit', description='Command to sanitize a reddit account.')
        parser.add_argument('client_id', help='Must be set. Client ID used to authenticate.')
        parser.add_argument('client_secret', help='Must be set. Client secret used to authenticate.')
        parser.add_argument('username', help='Must be set. Username of the account.')
        parser.add_argument('password', help='Must be set. Password of the account.')
        parser.add_argument('--two_factor', help='Set if you have two factor authentication on your account.')
        parser.add_argument('--file', help='Set if you have a config file containing the authentication details. Please have a look at example.env.yml for example on how to create one.')

        parsed_arguments = parser.parse_args(args)
        if parsed_arguments.file:
            config = load_config_from_file(parsed_arguments.file, 'reddit')
        else:
            config = {
                'client_id': parsed_arguments.client_id,
                'client_secret': parsed_arguments.client_secret,
                'username': parsed_arguments.username,
                'password': parsed_arguments.password,
                'two_factor': parsed_arguments.two_factor
            }

        routine = RedditRoutine(
            config.get('client_id'),
            config.get('client_secret'),
            config.get('username'),
            config.get('password'),
            config.get('two_factor'),
        )
        routine.sanitize_all()
