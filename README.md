> DSproject12
https://docs.google.com/document/d/1ukxB4uI04OOziNmmp8GzH3HQNXVdSmLxbXU6CvfXmUQ/edit#

- Data crawl - architecture;  Akshata/Ching-Han (Helen) <br> 
  3.6 ; Twitter account! -- Got my twitter account approved. Will Start coding from today (10/10/2018)  (Akshata Bhat)
  Collected Twitter Data from Home Profile using oAuth <br> 
  -( 05- 07/ Oct/ 2018) Ching-Han (Helen) <br>
    Received Twitter Dev account and started testing data crawl through Twitter API. <br>
  -(Keyword, Geolocation, Specific user’s post) <br>
    ( 12- 13/ Oct/ 2018) Ching-Han (Helen) <br>
  -Collected data from News website ( The Herald, The Scotsman, BBC Scotland) <br>
	  Date type: (Title, URL, Content) <br>
	  Date Storage: Waiting for MongoDB link to store the data for now. <br>
  -( 23/ Oct/ 2018) Ching-Han (Helen) <br>
    Updated the  news crawler of BBC Scotland (fix some bugs) <br>
  -(29-30/ Oct/ 2018) Ching-Han (Helen) <br>
    Updated the news crawl of The Herald. <br>
      1. Added new valuable (Title, Time, URL, Content) <br>
      2. Filter only top 5 sentences of news contents. <br>
      3. Save data in the text file. (there is an example file collected on Oct 30) <br>
    In process <br>
      automatically collect data every 6 hours. <br>
      update other two channels (The Scotsman, BBC Scotland) <br>
  -(06-07/ Nov/ 2018) Ching-Han (Helen) <br>
		 Updated the news crawl of The Herald, The Scotsman, BBC Scotland. <br>
  
- Database modelling - initial draft - (Yin) - MongoDB <br> 
  Created a mongodb on my laptop and developed some API for this project, such connect, insert and so on, and also discussed the data structure <br> 
  
- Entity paser - (Hu Liang- Brett) <br> 
  Looking into NLTK interface for Stanford NER <br> 
  https://nlp.stanford.edu/software/CRF-NER.shtml <br>  

- Group meeting(14/ Oct/ 2018): Akshata/ Ching-Han (Helen)/ Yin/ Hu Liang (Brett) <br>  
Working with Yin to structure the MongoDB for Twitter Data and News Data. We have decided we need the following columns:  
News: <br> 
ID, URL. Title, Text, Source <br>  
Twitter Data: <br> 
ID, Text, Time, Hashtags, Screen Name, Name, URL, Geo Enabled, Locatio,Organization <br> 

## Questions:  
1. Do we need to store this like an entity:number for news?  
2. Do we need to collect the likes, retweets and comments for twitter data and for the news articles for twitter?  
3. How can all 4 of us have access to the same instance of MongoDB from our laptops?  
