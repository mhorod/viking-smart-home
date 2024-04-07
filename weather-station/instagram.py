import os

from instagrapi import Client

class PostLikers:
    def __init__(self):
        ACCOUNT_USERNAME = os.getenv('INSTAGRAM_USERNAME')
        ACCOUNT_PASSWORD = os.getenv('INSTAGRAM_PASSWORD')

        self.POST_ID = "3340410970897959403"

        self.cl = Client()
        self.cl.login(ACCOUNT_USERNAME, ACCOUNT_PASSWORD)

        likers = self.cl.media_likers(self.POST_ID)

    def get_likers(self):
        return [liker.username for liker in self.cl.media_likers(self.POST_ID)]

    def get_comments(self):
        comments = self.cl.media_comments(POST_ID, 10)
        for c in comments:
            print(c.text)


