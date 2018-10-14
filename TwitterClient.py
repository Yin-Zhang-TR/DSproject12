import os
import sys
from tweepy import API
from tweepy import OAuthHandler

def get_twitter_auth():
    try:
        consumer_key='F0imGgOVzAzOpDuayoaIvSTC0'
        consumer_secret_key='qVW2Vh9tn7U4cMd3fpBTs1vhFyEMz5uScx1BYEKRbDNta3qRdc'
        access_token='81029819-2R4INZNvspGtCXJUYNn3Mk1hzyqrtXNmMUaurweVy'
        access_secret_token='3cS9tU4EwpU5iQ0RbYSbQoNNzeYpi7oq4IlvVU3lLNk9F'
        print("Connected Successfully")

    except KeyError:
        sys.stderr.write("Twitter_* environment variables not set\n")
        sys.exit(1)

    auth= OAuthHandler(consumer_key,consumer_secret_key)
    auth.set_access_token(access_token,access_secret_token)
    return auth

def get_twitter_client():
    auth=get_twitter_auth()
    client=API(auth)
    return client



