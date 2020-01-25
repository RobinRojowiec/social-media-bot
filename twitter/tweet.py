"""

IDE: PyCharm
Project: social-media-bot
Author: Robin
Filename: tweet.py
Date: 25.01.2020

"""
from datetime import datetime


class TweetSet:
    def __init__(self, twitter_handle, name, description, location):
        self.twitter_handle = twitter_handle
        self.profile_name = name
        self.profile_description = description
        self.profile_location = location
        self.crawled_at = datetime.now().strftime("%c")
        self.tweets = []

    def add_tweet(self, tweet):
        self.tweets.append(tweet)


class Tweet:
    def __init__(self, twitter_handle, text, url, date):
        self.twitter_handle = twitter_handle
        self.text = text
        self.url = url
        self.date = date
        self.hashtags = []
        self.mentions = []

    def add_hashtag(self, tag):
        self.hashtags.append(tag)

    def add_mention(self, mention):
        self.mentions.append(mention)

    def clean_text(self):
        for index, tag in enumerate(self.hashtags):
            self.text = self.text.replace(tag, "[%i]" % index)

        for index, mention in enumerate(self.mentions):
            self.text = self.text.replace(mention, "[%i]" % index)
