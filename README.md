# Twitter_Sentiment_Analysis


Introduction:
It is a Natural Language Processing problem in which Sentiment Analysis is performed by classifying positive and negative tweets using machine learning models for classification of tweets. 
Natural Language Processing (NLP) is a hotbed of data science research these days, and sentiment analysis is one of its prominent uses. From opinion surveys to the creation of entire marketing campaigns, text analysis has totally transformed the way organizations operate. Hundreds and thousands of text documents can be processed for sentiment in seconds, as opposed to the laborious way which would require a team to person such analysis manually.
Objective of the Project:
As shown on several social media platforms, many people have varied opinions (Positive/Negative/Neutral) about covid vaccination. To better comprehend this and reach a coherent conclusion, I performed a sentiment analysis on twitter data gathered from multiple hastags.

Data Cleaning and Processing and quick result:

1.	Data was extracted from twitter using Twitter API v2.
2.	All the tweets (unprocessed) were store on Mongo DB (docker container)
3.	Using python we Extracted tweets from Mongo DB for Transfomation.
4.	Using python we cleaned the text using RegX and NLP.
5.	Next, I used Vader Sentiment analysis tool box to analyse the tweets.
6.	All the sentiment and tweets is again loaded to psql for further analysis
7.	Also, made word cloud for sentiments with Positive, Negative and Neutral
8.	With word cloud on with positive data I found ‘GetVaccinated’ with greater prominence and for Negative data I found ‘Death’ repeating more offen.

How to work with this Repo?

1.	First git clone <repo>
  
2.	Make sure you have Python, docker, mongoDB and postgres SQL on your computer.
  
3.	Eg: On VS code open the folder which has docker-compose.yml file.
  
a.	Open terminal
b.	Type ‘docker-compose build’ this will start building the docker image 
c.	To check the docker images if its build or not!
i.	Type: ‘docker images’ to check the docker images
ii.	Next type: ‘docker ps -a’ to check docker container
If all the container and images are seen for this project, then you are good to go.
  
4.	Next, type ‘docker-compose up’ to run the ETL process
a.	It will extract tweets from twitter (get_tweets.py)
b.	Next it will extract the data from mongoDB
c.	Next, it will transform the data using RegX and NLP
d.	Next, Vader Sentiment analysis toolbox is used to get the twitter sentiments.
e.	Next word cloud will be plotted



