"""

IDE: PyCharm
Project: social-media-bot
Author: Robin
Filename: twitter_sample.py
Date: 25.01.2020

"""
import json
import os
from datetime import datetime
from datetime import timedelta

import tweepy
from dotenv import load_dotenv
from tweepy import Cursor

from twitter.tweet import Tweet, TweetSet

load_dotenv()

# Authenticate to Twitter
auth = tweepy.OAuthHandler(os.getenv("TWITTER_CLIENT_ID"), os.getenv("TWITTER_CLIENT_SECRET"))
auth.set_access_token(os.getenv("TWITTER_ACCESS_TOKEN"), os.getenv("TWITTER_ACCESS_TOKEN_SECRET"))

api = tweepy.API(auth, wait_on_rate_limit=True,
                 wait_on_rate_limit_notify=True)

try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")

twitter_handle = os.getenv("TWITTER_HANDLE")
user = api.get_user(twitter_handle)

print("User details:")
print(user.name)
print(user.description)
print(user.location)

tweet_set = TweetSet(twitter_handle, user.name, user.description, user.location)

hashtags = []
mentions = []
tweet_count = 0
end_date = datetime.utcnow() - timedelta(days=30)
for status in Cursor(api.user_timeline, id=twitter_handle).items():
    tweet_count += 1
    tweet = Tweet(twitter_handle, status.text, "", status.created_at.strftime("%c"))
    if hasattr(status, "entities"):
        entities = status.entities
        if "hashtags" in entities:
            for ent in entities["hashtags"]:
                if ent is not None:
                    if "text" in ent:
                        hashtag = ent["text"]
                        if hashtag is not None:
                            tweet.add_hashtag(hashtag)
        if "user_mentions" in entities:
            for ent in entities["user_mentions"]:
                if ent is not None:
                    if "screen_name" in ent:
                        name = ent["screen_name"]
                        if name is not None:
                            tweet.add_mention(name)
    if status.created_at < end_date:
        break
    tweet.clean_text()
    tweet_set.add_tweet(tweet.__dict__)

with open("tweets_%s.json" % twitter_handle, "w+", encoding="utf8") as json_file:
    json_file.write(json.dumps(tweet_set.__dict__, indent=2, ensure_ascii=False))
