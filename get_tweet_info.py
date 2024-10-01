import os
import tweepy

def get_token_from_file(filename):
    try:
        with open(filename, 'r') as file:
            token = file.read().strip()
            if not token:
                raise ValueError("The token is empty")
            return token
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    except Exception as e:
        print(f"Error reading token from file: {e}")

TEST_TOKEN = get_token_from_file('./TWEET_TOKEN.txt')
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

