from cleo import Application
from sanitize.commands.discord_command import DiscordCommand
from sanitize.commands.reddit_command import RedditCommand

if __name__ == '__main__':
    application = Application()
    application.add(DiscordCommand())
    application.add(RedditCommand())
    application.run()
