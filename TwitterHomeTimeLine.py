from tweepy import Cursor
import json
from TwitterClient import get_twitter_client

if __name__=='__main__':
    client=get_twitter_client()

with open('home_timeline.jsonl','w') as f:
    for status in Cursor(client.home_timeline).items(10):
        for page in Cursor(client.home_timeline,count=200).pages(2):
            for status in page:
                f.write(json.dumps(status._json)+"\n")

