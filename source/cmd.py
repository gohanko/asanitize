import argparse
from .plugins.discord.routines import DiscordRoutines

commands = [
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

routines = [
    {
        'service': 'discord',
        'routine': DiscordRoutines
    }
]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    for command in commands:
        parser.add_argument(command['short_arg'], command['long_arg'], **command['named_parameters'])

    args = parser.parse_args()
    for routine in routines:
        if args.service == routine['service']:
            routine['routine'](args.token)