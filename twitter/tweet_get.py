#!/usr/bin/env python
# -*- coding: utf-8 -*-
from requests_oauthlib import OAuth1Session, OAuth1
import json
import requests
import configparser

'''
twitter_api.ini

[twtter_api]
consumer_key=
consumer_key_secret=
access_token=
access_token_secret=

'''
config_file="twitter_api.ini"                                                                                                                                                                                     
config = configparser.SafeConfigParser()                                                                                                                                                                          
config.read(config_file, encoding='utf-8-sig')                                                                                                                                                                    
                                                                                                                                                                                                                  
consumer_key = config.get("twtter_api", "consumer_key")                                                                                                                                                           
consumer_key_secret = config.get("twtter_api", "consumer_key_secret")                                                                                                                                             
access_token = config.get("twtter_api", "access_token")                                                                                                                                                           
access_token_secret = config.get("twtter_api", "access_token_secret")    


def search_key(word):

    url = "https://api.twitter.com/1.1/search/tweets.json?count=100&lang=ja&q=" + word
    auth = OAuth1(consumer_key, consumer_key_secret, access_token, access_token_secret)
    response = requests.get(url, auth = auth)
    data = response.json()['statuses']
    return data

def get_user_tweet(user):

    url = "https://api.twitter.com/1.1/statuses/user_timeline.json?count=100&lang=ja&screen_name=" + user
    auth = OAuth1(consumer_key, consumer_key_secret, access_token, access_token_secret)
    response = requests.get(url, auth = auth)
    print(response.json())
    data = response.json()
    return data

if __name__ == "__main__":

    word = "ポケットモンスター"
    #data = search_key(word)
    user = "mottoatuku"
    data = get_user_tweet(user)

    for tweet in data:
      try:
          print(tweet["id_str"])
          print(tweet["text"].replace("\n", ""))
          print(tweet["created_at"])
      except:
          print("Error")
