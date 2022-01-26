import tweepy
from tweepy import user
from credentials import *
import logging
import pprint
import pymongo
import pandas as pd
import time
### Authentication ###
client = tweepy.Client(bearer_token=BEARER_TOKEN_Aca,consumer_key=API_KEY_Aca,consumer_secret=API_KEY_SECRET_Aca,
access_token=ACCESS_TOKEN_Aca,access_token_secret=ACCESS_TOKEN_SECRET_Aca, wait_on_rate_limit=True)

# client = tweepy.Client(bearer_token=BEARER_TOKEN,consumer_key=API_KEY,consumer_secret=API_KEY_SECRET,
# access_token=ACCESS_TOKEN,access_token_secret=ACCESS_TOKEN_SECRET)


print('###################################################################################################')
if client:
    logging.critical('\nAuthentication OK')
else:
    logging.critical('\nVerify your credentials')

myclient = pymongo.MongoClient("mymongo" ,port= 27017)

mydb = myclient["tweetcollector"]
mycol = mydb["Dogecoin_test"]

print('#############################################################################################')
tweets = {}
query1 = 'dogecoin -is:retweet lang :en'
paginator = tweepy.Paginator(client.search_all_tweets,
                             tweet_fields=['id','created_at','geo','text'],
                             user_fields = ['location'],
                             query=query1,
                             max_results=500,
                             start_time = '2021-01-20T00:00:00Z',
                             end_time = '2021-01-22T00:00:00Z'
                             ).flatten(limit=500) # client.search_recent_tweets,
#print(paginator)
for i,tweet in enumerate(paginator):

    tweets['ID'] = tweet.id
    tweets['tweet'] = tweet.text
    tweets['created_at'] = tweet.created_at
    mycol.update_one(tweets,{'$set':tweets},upsert=True)
            
    #print(tweets)
time.sleep(25)
print('Tweets recored:',i+1)




