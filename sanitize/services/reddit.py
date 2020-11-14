import praw
from prawcore import ResponseException
from sanitize.common import random_word, create_logger

class Routine:
    def __init__(self, client_id, client_secret, username, password, two_factor=None):
        self.logger = create_logger(__name__)
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
            user_agent='https://github.com/gohanko/sanitize'
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
                self.logger.info(
                    '[%s] Comment ID %s by %s',
                    self.sanitize_all.__name__,
                    comment,
                    self.username,
                )

                comment.edit(random_word())
                comment.delete()

            submissions = self.reddit.redditor(self.username).submissions.new(limit=None)
            for submission in submissions:
                self.logger.info(
                    '[%s] Submission ID %s by %s',
                    self.sanitize_all.__name__,
                    submission,
                    self.username,
                )

                submission.edit(random_word())
                submission.delete()

            if not comments or not submissions:
                break

        return True
