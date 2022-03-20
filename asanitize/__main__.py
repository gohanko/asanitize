import sys
from asanitize.user_interface.cli import CommandLineInterface
from asanitize.user_interface.gui import start_app

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        CommandLineInterface()
    else:
        start_app()
