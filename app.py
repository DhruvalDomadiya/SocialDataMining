# -*- coding: utf-8 -*-
"""
Created on Sat Oct  9 12:37:49 2021

@author: HELLO
"""

from flask import Flask, request, render_template
from pymongo import MongoClient
import tweepy
import praw

app = Flask(__name__)

#Credentials For Twitter
consumer_key= 'RiaEWWcGL1uwaR3ySnm85MtyV'
consumer_secret= 'rabVWOMLxuq53NtHd5GfVdkOLVxOC03AIOvJEaG05SI8bhkJmh'
access_token= '3472955293-O357zZyUQYcrBOskVMu6DYzCFtIfh8inQtcrjyr'
access_token_secret= 'FVJ7qknqSwk6B6FwhiQL3U5iqUy9GJRD6lB38lX7R1eir'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

#Credential For Reddit
redditAuth = praw.Reddit(client_id = 'mnx1cjnQ2tWcipkj4UM7SA'
                    , client_secret = 'M-wXIuBGi4UeWGvb3mOTf-OCgBKbLQ'
                    , username = 'Dhruval2809'
                    , password = 'Dhru@9824900962'
                    , user_agent = 'XYZ' )
RedditUsername = "Dhruval2809"

@app.route('/')

def home():
    return render_template('Home.html')

@app.route('/twitterPost', methods =['GET','POST'])
def postTweet():
        
    api = tweepy.API(auth, wait_on_rate_limit=True)

    client = MongoClient('mongodb+srv://Dhruval:dhru9824900962@cluster0.5wprs.mongodb.net/SDM?ssl=true&ssl_cert_reqs=CERT_NONE')
    db = client['SDM']
    
    if request.method == 'POST':
        tweet = request.form['twitterText']
        post = api.update_status(tweet)
        #print(post)
        db.TwitterData.insert_one({'Id':post.id_str,
                                   'Source':post.source,
                                   'tweet_text':post.text,
                                   'time':post.created_at,
                                   'likes':post.favorite_count
                                   })

    return render_template('Twitter.html')


@app.route('/redditPost', methods =['GET','POST'])
def postReddit():
    
    client = MongoClient('mongodb+srv://Dhruval:dhru9824900962@cluster0.5wprs.mongodb.net/SDM?ssl=true&ssl_cert_reqs=CERT_NONE')
    db = client['SDM']
    
    if request.method == 'POST':
        title = str(request.form['redditTitle'])
        desc = str(request.form['redditDes'])
        data = redditAuth.subreddit('u_Dhruval2809').submit(title, desc )
        db.RedditData.insert_one({'Id':data.id,
                                   'Title':data.title,
                                   'Description':data.selftext,
                                   'Score':data.score,
                                   'Timestamp':data.created
                                   })
        
    return render_template('Reddit.html')

if __name__ == "__main__":
    app.run() 