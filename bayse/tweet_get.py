#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
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

    url = "https://api.twitter.com/1.1/search/tweets.json?count=200&lang=ja&q=" + word
    auth = OAuth1(consumer_key, consumer_key_secret, access_token, access_token_secret)
    response = requests.get(url, auth = auth)
    data = response.json()['statuses']
    return data

def get_user_tweet(user, max_id=0):

    url = "https://api.twitter.com/1.1/statuses/user_timeline.json?count=200&lang=ja&screen_name=" + user
    if max_id > 1 :
      url = url + "&max_id=" + str(max_id)
    auth = OAuth1(consumer_key, consumer_key_secret, access_token, access_token_secret)
    response = requests.get(url, auth = auth)
    data = response.json()
    return data

if __name__ == "__main__":

    #word = "ポケットモンスター"
    #data = search_key(word)
    #user = "mottoatuku"
    #data = get_user_tweet(user)
    
    arguments = sys.argv
    if len(arguments) == 1:
      print ("Usage: user_name")
      exit(0)
    user = arguments[1]
    print(user)
    file = "tweet_" + user + ".txt"
    f = open(file, 'w', encoding='utf-8-sig')
    get_count = 2000
    max_id = 0;
    count = 0;
    while True and (count < get_count):
      max_id-=1
      data = get_user_tweet(user, max_id)
      for tweet in data:
        count+=1
        try:
            max_id = tweet["id"]
            created_at = tweet["created_at"] 
            text = tweet["text"].replace("\n", "") + "\n" 
            f.write(text)
        except:
            print("Error")
        print("{0} : {1} : {2}".format(count, created_at, text))
    f.close()

