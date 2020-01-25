"""

IDE: PyCharm
Project: social-media-bot
Author: Robin
Filename: instabot_sample.py
Date: 24.01.2020

"""
import os

from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()

username, password = os.getenv("INSTA_USER"), os.getenv("INSTA_PASSWORD")

from instabot import Bot

bot = Bot(filter_users=False)

bot.login(username=username, password=password)

medias = bot.get_hashtag_medias('plantmom')
for media in tqdm(medias):
    bot.like(media)
    print(bot.get_link_from_media_id(media))
bot.logout()

# bot.logout()
# user_id = bot.get_user_id_from_username("RobiNLPHood")
# user_info = bot.get_user_info(user_id)
# print(user_info['biography'])
