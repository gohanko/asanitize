from ast import parse
import sys
import argparse
from asanitize.config import DiscordConfiguration, RedditConfiguration, ConfigurationManager
from asanitize.services.discord.sanitize import sanitize
from asanitize.services.reddit.reddit import RedditRoutine


# https://chase-seibert.github.io/blog/2014/03/21/python-multilevel-argparse.html
class CommandLineInterface:
    def __init__(self):
        self.configuration_manager = ConfigurationManager()

        parser = argparse.ArgumentParser(
            prog='asanitize.py',
            description='Software to sanitize your online accounts.')
        parser.add_argument(
            'service',
            help='Select which service to be sanitize.')

        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.service):
            print('Unrecognized service')
            parser.print_help()
            exit(1)

        getattr(self, args.service)(sys.argv[2:])

    def discord(self, args):
        parser = argparse.ArgumentParser(
            prog='asanitize.py discord',
            description='Command to sanitize a discord account.')
        parser.add_argument(
            'token',
            help='Required. Authentication token of a discord account.')
        parser.add_argument(
            'channel',
            help='Required. Either a specific channel id or \'all\' to sanitize all.')
        parser.add_argument(
            '--useconfig',
            help='Optional. File containing authentication token and channel ids.')
        parser.add_argument(
            '--fastmode',
            help='Optional. Just deletes message instead of editing before deleting if set.',
            action=argparse.BooleanOptionalAction)

        parsed_arguments = parser.parse_args(args)
        if parsed_arguments.useconfig:
            config = self.configuration_manager.get_service_config('discord')
        else:
            config = DiscordConfiguration(
                token=parsed_arguments.token,
                channels_to_sanitize=[parsed_arguments.channel],
                fastmode=parsed_arguments.fastmode)

        sanitize(
            config.token,
            config.channels_to_sanitize,
            None,
            config.fastmode)

    def reddit(self, args):
        parser = argparse.ArgumentParser(
            prog='asanitize.py reddit',
            description='Command to sanitize a reddit account.')
        parser.add_argument(
            'client_id',
            help='Must be set. Client ID used to authenticate.')
        parser.add_argument(
            'client_secret',
            help='Must be set. Client secret used to authenticate.')
        parser.add_argument(
            'username',
            help='Must be set. Username of the account.')
        parser.add_argument(
            'password',
            help='Must be set. Password of the account.')
        parser.add_argument(
            '--two_factor',
            help='Set if you have two factor authentication on your account.')
        parser.add_argument(
            '--file',
            help='Optional. File containing authentication secrets.')

        parsed_arguments = parser.parse_args(args)
        if parsed_arguments.file:
            config = self.configuration_manager.get_service_config('reddit')
        else:
            config = RedditConfiguration(
                client_id=parsed_arguments.client_id,
                client_secret=parsed_arguments.client_secret,
                username=parsed_arguments.username,
                password=parsed_arguments.password)

        routine = RedditRoutine(
            config.client_id,
            config.client_secret,
            config.username,
            config.password,
            parsed_arguments.two_factor)

        routine.sanitize_all()
