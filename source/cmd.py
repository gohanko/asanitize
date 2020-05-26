"""
    cmd.py - Commandline Parser

    This module handles the cli part of the application.

    See COMMANDS for available commands and see ROUTINES
    for the routines associated with the command.
"""

import argparse
from .plugins.discord.routines import DiscordRoutines

if __name__ == '__main__':
    COMMANDS = [
        {
            'short_arg': '-t',
            'long_arg': '--token',
            'named_parameters': {
                'type': str,
                'required': True,
                'help': 'The authorization token to access the account.'
            },
        },
        {
            'short_arg': '-s',
            'long_arg': '--service',
            'named_parameters': {
                'type': str,
                'required': True,
                'help': 'The service in which the account you want to sanitize resides.'
            },
        }
    ]

    ROUTINES = [
        {
            'service': 'discord',
            'routine': DiscordRoutines
        }
    ]

    PARSER = argparse.ArgumentParser()
    for COMMAND in COMMANDS:
        PARSER.add_argument(
            COMMAND['short_arg'],
            COMMAND['long_arg'],
            **COMMAND['named_parameters']
        )

    ARGS = PARSER.parse_args()
    for ROUTINE in ROUTINES:
        if ARGS.service == ROUTINE['service']:
            ROUTINE['routine'](ARGS.token).run()
