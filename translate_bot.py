import pandas as pd
from tweepy.auth import OAuthHandler
import tweepy
from datetime import datetime, date, timedelta
import re
import pytz
import time
from deep_translator import GoogleTranslator


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
                #get the original tweets
                tweet = api.get_status(mention.in_reply_to_status_id)
                print(tweet.text)
                #deploy the translator and get the translated text
                target = '新鲜出炉的中文翻译：'+GoogleTranslator(source='auto', target='zh-CN').translate(tweet.text)
                print(target)
                #send the tweet
                s = api.update_status(status = target, in_reply_to_status_id = mention.id, auto_populate_reply_metadata=True)
                print('already sent')
                already.append(mention.id)
            else:
                continue
        time.sleep(60)

bot()
