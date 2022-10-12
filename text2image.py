import numpy as np
import pandas as pd
from tweepy.auth import OAuthHandler
import tweepy
from datetime import datetime, date, timedelta
import deepl
import matplotlib.pyplot as plt
import re
import pytz
from deep_translator import GoogleTranslator
import requests
import os
import time

#read tokens
list = []
with open('token.txt') as f:
    for lines in f:
        line = lines.strip()
        list.append(line)
consumer_key,consumer_secret,access_token, access_token_secret = list

#login and get api
auth = OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
#request current time for later use
timeZ_London = pytz.timezone('Africa/Accra')
dt_London = datetime.now(timeZ_London).replace(tzinfo=None)

#create image and send
def tweet_image(api, text, message,mention):
    #request url
    r = requests.post(
    "https://api.deepai.org/api/text2img",
    data={
        'text': text,
    },
    headers={'api-key': 'quickstart-QUdJIGlzIGNvbWluZy4uLi4K'}
)
    url = r.json()['output_url']
    filename = 'temp.jpg'
    #download it to local
    request = requests.get(url, stream=True)
    if request.status_code == 200:
        with open(filename, 'wb') as image:
            for chunk in request:
                image.write(chunk)
        #send it
        media= api.media_upload(filename)
        post_result = api.update_status(status=message, media_ids=[media.media_id],in_reply_to_status_id = mention.id, auto_populate_reply_metadata=True)
        os.remove(filename)
    else:
        print("Unable to download image")


def bot():
    already = []
    while True:
        #after each loop,update timeline
        mentions = api.mentions_timeline() 
        for mention in mentions:
            #only send to those mentions which tweeted after service launched and never sent before
            if (mention.created_at-dt_London).total_seconds()>=0 and mention.id not in already:
                print('Request Details')
                print(mention.text)
                print(mention.id)
                print(mention.in_reply_to_status_id)
                print(mention.in_reply_to_screen_name)
                text = mention.text
                message = 'check it out bro'
                tweet_image(api, text, message,mention)
            else:
                continue
        time.sleep(60)

bot()