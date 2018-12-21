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
import pymongo,json
from pymongo import InsertOne, DeleteOne, ReplaceOne
from nltk.tag import StanfordNERTagger
eng_tagger = StanfordNERTagger(model_filename=r'/scratch2/project/stanford-ner-2018-10-16/classifiers/english.all.3class.distsim.crf.ser.gz',path_to_jar=r'/scratch2/project/stanford-ner-2018-10-16/stanford-ner.jar')
client = pymongo.MongoClient(host='localhost', port=27017)
db_twitter=client.TWITTER_DB
import queue
import threading
import datetime
exitFlag = 0

class myThread (threading.Thread):
    def __init__(self, threadID, name, q, rlock):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q
        self.rl = rlock
    def run(self):
        print ("Starting Thread: " + self.name)
        process_data(self.name, self.q, self.rl)
        print ("Exiting Thread: " + self.name)

def process_data(threadName, q, rlock):
    while not exitFlag:
        queueLock.acquire()
        if not workQueue.empty():
            item = q.get()
            queueLock.release()
            #print ("%s processing %s" % (threadName, item['text']))
            collection_twitter = db_twitter.Twitter1204_REMOVENOISE_NER_MultiThread
#             for item in db_twitter.Twitter1204_REMOVENOISE.find():

            rlock.acquire()
            doc=eng_tagger.tag(item['text'].split())
            rlock.release()
        
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
        else:
            queueLock.release()
        time.sleep(1)

threadList = ["Thread-"+str(i) for i in range(1,101)]
rlock = threading.RLock()
queueLock = threading.Lock()
workQueue = queue.Queue()
threads = []
threadID = 1

for tName in threadList:
    thread = myThread(threadID, tName, workQueue, rlock)
    thread.start()
    threads.append(thread)
    threadID += 1

starttime = datetime.datetime.now()
queueLock.acquire()
for word in db_twitter.Twitter1204_REMOVENOISE.find():
    #print(word)
    workQueue.put(word)
queueLock.release()

while not workQueue.empty():
    pass

exitFlag = 1

for t in threads:
    t.join()
print ("Starting Main Thread!!!")

endtime = datetime.datetime.now()
print("Time used:", endtime - starttime)