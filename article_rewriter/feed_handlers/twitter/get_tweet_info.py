import os

import tweepy

from article_rewriter.utils.utils import get_api_key

TEST_TOKEN = get_api_key('./TWEET_TOKEN.txt')
client = tweepy.Client(bearer_token=TEST_TOKEN)


class UserData:
    fields = {}


class TweetExtractor:
    def __init__(self, t_client) -> None:
        self.__client = t_client
        self._data = UserData

    def get_user(self, username):
        return self.__client.get_user(username=username)

    def extract_data(self):
        pass


my_tweet_extractor = TweetExtractor(client)
user = my_tweet_extractor.get_user("Haberturk")

tweet_fields = [
    "attachments", "context_annotations", "conversation_id", "entities", "geo",
    "in_reply_to_user_id", "lang", "public_metrics", "possibly_sensitive",
    "referenced_tweets", "source", "withheld"
]
