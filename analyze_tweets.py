"""

IDE: PyCharm
Project: social-media-bot
Author: Robin
Filename: analyze_tweets.py
Date: 25.01.2020

"""
import json
import os
from collections import defaultdict
from datetime import datetime

import dotenv
import pandas as pd
import spacy
from matplotlib import pyplot

nlp = spacy.load('en_core_web_sm')


def lexical_analysis(tweets_filepath):
    words_per_document = defaultdict(set)
    with open(tweets_filepath, 'r', encoding='utf8') as json_file:
        tweet_set = json.load(json_file)
        for tweet in tweet_set["tweets"]:
            text = tweet["text"]
            analyzed_text = nlp(text)

            for token in analyzed_text:
                words_per_document[token.lemma_].add(tweet["tweet_id"])

    kv_list = words_per_document.items()
    print(kv_list)


def general_stats(tweets_filepath):
    with open(tweets_filepath, 'r', encoding='utf8') as json_file:
        tweets = json.load(json_file)["tweets"]
        for tweet in tweets:
            tweet["date"] = datetime.strptime(datetime.strptime(tweet["date"], "%c").strftime('%d.%m.%y'), '%d.%m.%y')

    series = pd.DataFrame.from_records(tweets, index="tweet_id", exclude=['hashtags', 'url', 'text'])

    grouped = series.groupby('date').count()
    grouped.plot()
    pyplot.show()

    mentions = series["mentions"].apply(pd.Series)
    mentions = mentions.rename(columns=lambda x: 'mention_' + str(x))
    print(mentions)

    concat = pd.concat([series[:], mentions[:]], axis=1)
    concat = concat.groupby('date').count()
    print(concat)

    concat.plot()
    pyplot.show()


if __name__ == '__main__':
    dotenv.load_dotenv()
    tweets_file = os.getenv('TWITTER_DATA')

    general_stats(tweets_file)
    # lexical_analysis(tweets_file)
