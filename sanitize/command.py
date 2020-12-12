from cleo import Application
from sanitize.discord.command import DiscordCommand
from sanitize.reddit.command import RedditCommand

def create_cleo_app():
    application = Application()
    application.add(DiscordCommand())
    application.add(RedditCommand())
    return application
