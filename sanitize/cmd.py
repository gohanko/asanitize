from cleo import Application
from sanitize.commands.discord_command import DiscordCommand


application = Application()
application.add(DiscordCommand())

if __name__ == '__main__':
    application.run()