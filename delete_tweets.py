from tweepy.auth import OAuthHandler
import tweepy
import sys


def delete(user):
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

    #get all of your tweets
    userID = user
    user = api.get_user(userID)
    tweets = api.user_timeline(screen_name=userID, 
                            count=200,
                            tweet_mode = 'extended'
                            )

    while True:
        count=0
        tweets = api.user_timeline(screen_name=userID, 
                    count=200,
                    tweet_mode = 'extended'
                    )
        for info in tweets:
            print("ID: {}".format(info.id))
            try:
                #try to delete
                api.destroy_status(info.id)
            except:
                #if error, refresh your tweets timeline and count all over again, count from 0 again
                print('Err')
                break
            count+=1
        if count == len(tweets):
            #finished
            break

delete(sys.argv[1])