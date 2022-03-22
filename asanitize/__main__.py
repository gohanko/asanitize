import sys
from asanitize.cli import CommandLineInterface
from asanitize.gui import start_app


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        CommandLineInterface()
    else:
        start_app()
