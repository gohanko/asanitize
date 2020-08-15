from cleo import Application
from sanitize.commands.discord_command import DiscordCommand


if __name__ == '__main__':
    application = Application()
    application.add(DiscordCommand())
    application.run()