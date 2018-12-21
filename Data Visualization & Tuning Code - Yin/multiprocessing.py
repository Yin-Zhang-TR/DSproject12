import multiprocessing
import nltk
import numpy as np
import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time
import json
import pymongo
from pymongo import MongoClient,ASCENDING, DESCENDING
import json
from pymongo import InsertOne, DeleteOne, ReplaceOne
from nltk.tag import StanfordNERTagger
eng_tagger = StanfordNERTagger(model_filename=r'/scratch2/project/stanford-ner-2018-10-16/classifiers/english.all.3class.distsim.crf.ser.gz',path_to_jar=r'/scratch2/project/stanford-ner-2018-10-16/stanford-ner.jar')
#client = pymongo.MongoClient(host='localhost', port=27017)
#db_twitter=client.test
import queue
import threading
import datetime
exitFlag = 0

def process_data(item):
    #print(db_twitter)
    client = pymongo.MongoClient(host='localhost', port=27018, connect=False)
    db_twitter=client.TWITTER_DB
    
    collection_twitter = db_twitter.Twitter1204_REMOVENOISE_NER

    doc=eng_tagger.tag(item['text'].split())
    #print(doc)
    orgstr = ""
    locstr = ""
    pstr = ""
    for i in range(len(doc)):
        if 'PERSON' in doc[i][1]:
            per =doc[i][0]
            pstr = pstr + "," + per
        #tag = 0
        else:
            if 'ORGANIZATION' in doc[i][1]:
                org =doc[i][0]
                orgstr = orgstr + "," + org
            else:
                if 'LOCATION' in doc[i][1]:
                    loc =doc[i][0]
                    locstr = locstr + "," + loc

    if (orgstr is not "") or (locstr is not "") or (pstr is not ""):
        id=item['id']
        created_at=item['created_at']
        entities=item['entities']
        geo=item['geo']
        place=item['place']
        coordinates=item['coordinates']
        timestamp_ms=item['timestamp_ms']
        result=collection_twitter.insert_one({"id":id,"ORGANIZATION": orgstr,"LOCATION": locstr,"PERSON": pstr,"ENTITIES":orgstr+locstr+pstr,
                                  "created_at":created_at,"entities":entities,"geo":geo,"coordinates":coordinates,
                                 "place":place,"timestamp_ms":timestamp_ms})
    
    client.close()


if __name__ == "__main__":
    client = pymongo.MongoClient(host='localhost', port=27018)
    db_twitter=client.TWITTER_DB

    starttime = datetime.datetime.now()
    
    print("Starting Filling Queue!\n")
    manager = multiprocessing.Manager()
    queue = manager.Queue()
    for word in db_twitter.Twitter1204_REMOVENOISE.find():
        queue.put(word)
    client.close()
    print("Finished Filling Queue!\n")

    pool = multiprocessing.Pool(processes = 30)
    while not queue.empty():
        item = queue.get()
        #print(db_twitter)
        pool.apply_async(process_data, (item, ))

    print("Mark~ Mark~ Mark~~~~~~~~~~~~~~~~~~~~~~")
    
    pool.close()
    pool.join() 
#     queue.close()
#     queue.join_thread()
    print("Sub-process(es) done.")
    
    endtime = datetime.datetime.now()
    print("Time used:",endtime - starttime)