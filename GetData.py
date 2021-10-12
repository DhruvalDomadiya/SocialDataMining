# -*- coding: utf-8 -*-
"""
Created on Sun Oct 10 16:29:08 2021

@author: HELLO
"""

from pymongo import MongoClient
import tweepy
import praw
import pandas as pd

#Credentials For Twitter
consumer_key= 'RiaEWWcGL1uwaR3ySnm85MtyV'
consumer_secret= 'rabVWOMLxuq53NtHd5GfVdkOLVxOC03AIOvJEaG05SI8bhkJmh'
access_token= '3472955293-O357zZyUQYcrBOskVMu6DYzCFtIfh8inQtcrjyr'
access_token_secret= 'FVJ7qknqSwk6B6FwhiQL3U5iqUy9GJRD6lB38lX7R1eir'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)
TwitterUsername = "dhrudomadiya"

#Connection to the MongoDB
client = MongoClient('mongodb+srv://Dhruval:dhru9824900962@cluster0.5wprs.mongodb.net/SDM?ssl=true&ssl_cert_reqs=CERT_NONE')
db = client['SDM']

#Get user tweets from twitter profile
def getTweets(username):
    Id, Source, tweet_text, time, likes = [],[],[],[],[]
    for i in tweepy.Cursor(api.user_timeline, tweet_mode="extended").items():
        Id.append(i.id)
        Source.append(i.source)
        tweet_text.append(i.full_text)
        time.append(i.created_at)
        likes.append(i.favorite_count)
    
    data = {"Id":Id, "Source":Source, "tweet_text":tweet_text, "time":time, "likes":likes}
    #print(data)
    df = pd.DataFrame(data=data)
    #print(df)
    db.TwitterData.delete_many({})
    db.TwitterData.insert_many(df.to_dict('records'))
    

#Credential For Reddit
redditAuth = praw.Reddit(client_id = 'mnx1cjnQ2tWcipkj4UM7SA'
                    , client_secret = 'M-wXIuBGi4UeWGvb3mOTf-OCgBKbLQ'
                    , username = 'Dhruval2809'
                    , password = 'Dhru@9824900962'
                    , user_agent = 'XYZ' )
RedditUsername = "Dhruval2809"

#Get Reddit Data
def getReddits(RedditUsername):
    #user = redditAuth.redditor(RedditUsername)
    #sub = user.submissions.top()
    Posts = []
    for post in redditAuth.redditor(RedditUsername).submissions.top():
        Posts.append({"ID":post.id,
                     "Title":post.title,
                     "Description":post.selftext,
                     "Score":post.score,
                     "Timestamp":post.created})

    #print(Posts)
    db.RedditData.delete_many({})
    df = pd.DataFrame(Posts)
    db.RedditData.insert_many(df.to_dict('records'))

getTweets(TwitterUsername)
getReddits(RedditUsername)