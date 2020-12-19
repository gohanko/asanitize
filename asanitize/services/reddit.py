import praw
from prawcore import ResponseException
from asanitize.common import random_word

class RedditRoutine:
    def __init__(self, client_id, client_secret, username, password, two_factor=None):
        self.username = username
        self.reddit = self._login(
            client_id, 
            client_secret,
            username,
            password,
            two_factor,
        )
        self.reddit.validate_on_submit = True

    def _login(self, client_id, client_secret, username, password, two_factor):
        if two_factor:
            password = '{}:{}'.format(password, two_factor)

        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            username=username,
            password=password,
            user_agent='https://github.com/gohanko/asanitize'
        )

        return reddit

    def is_logged_in(self):
        try:
            return self.reddit.user.me() == self.username
        except ResponseException:
            return False

    def sanitize_all(self):
        while True:
            comments = self.reddit.redditor(self.username).comments.new(limit=None)
            for comment in comments:
                print('Editing and deleting the following comment by {}: {}'.format(self.username, comment))
                comment.edit(random_word())
                comment.delete()

            submissions = self.reddit.redditor(self.username).submissions.new(limit=None)
            for submission in submissions:
                print('Editing and deleting the following submission by {}: {}'.format(self.username, submission))
                submission.edit(random_word())
                submission.delete()

            if not comments and not submissions:
                break

        return True
