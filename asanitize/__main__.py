import sys
from asanitize.command_line_interface import CommandLineInterface


if __name__ == '__main__':
    try:
        CommandLineInterface()
    except KeyboardInterrupt:
        print('CTRL + C was pressed. Stopping the script.')
        sys.exit(0)
