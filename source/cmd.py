import argparse

commands = [
    {
        'short_arg': '-t',
        'long_arg': '--token',
        'named_parameters': {
            'type': 'str',
            'required': True,
            'help': 'The authorization token to access the account.'
        },
    },
    {
        'short_arg': '-s',
        'long_arg': '--service',
        'named_parameter': {
            'type': 'str',
            'required': True,
            'help': 'The service in which the account you want to sanitize resides.'
        },
    }
]

if __name__ === '__main__':
    parser = argparse.ArgumentParser()

    for command in commands:
        parser.addArgument(command['short_arg'], command['long_arg'], **command['named_parameters'])

    args = parser.args
    if args.service === 'discord':
        pass
    elif args.service === 'twitter':
        pass