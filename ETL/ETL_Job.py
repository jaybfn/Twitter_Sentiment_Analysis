# Importing libraries
import pymongo
from pymongo import MongoClient
import pandas as pd
import numpy as np
import string
import re
import os
import time
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import TreebankWordTokenizer
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
from sklearn.feature_extraction import _stop_words
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import wordcloud
from wordcloud import WordCloud
from sqlalchemy import create_engine
import seaborn as sns
import matplotlib.pyplot as plt
import psycopg2

lemmatizer = WordNetLemmatizer()
tokenizer= TreebankWordTokenizer()
skl_stopwords=_stop_words.ENGLISH_STOP_WORDS

time.sleep(60)
## MONGODB
HOST_MDB = 'mymongo' # if in docker it would be the container name
PORT_MDB = 27017
# Connection string
conn_string_mdb = f"mongodb://{HOST_MDB}:{PORT_MDB}" 
client = MongoClient(conn_string_mdb)

## POSTGRES
USERNAME_PG = 'postgres'
PASSWORD_PG = 'postgres'
HOST_PG = 'sentiment_tweet' # if in docker it would be the container name
PORT_PG = 5432
DATABASE_NAME_PG = 'posty_tweets'

# Connection string
conn_string_pg = f"postgresql://{USERNAME_PG}:{PASSWORD_PG}@{HOST_PG}:{PORT_PG}/{DATABASE_NAME_PG}" 
pg = create_engine(conn_string_pg,client_encoding='utf8')

pg.execute('''
CREATE TABLE IF NOT EXISTS doge_table (
    neg numeric,
    new numeric,
    pos numeric,
    compound numeric,
    tweet TEXT,
    Sentiment_label TEXT
);
''')


def extract(database, collection):
    global sample_lst
    sample_lst = []
    mydb = client[database]# "tweetcollector"
    mycol = mydb[collection]  # "vaxdata"
    tweets = list(mycol.find())
    tweets_df = pd.DataFrame(data = tweets)
    sample_text = tweets_df.tweet
    sample_lst = sample_text.tolist()
    return sample_lst

#extract("tweetcollector","vaxdata")

# # 4 Text Cleaning and Processing

def transform(tweet_list):
    
    text_clean = []
    for i in tweet_list:
        prohibitedWords = ['Antivax','antivax','People','Covid','people','covid']
        text = re.compile('|'.join(map(re.escape, prohibitedWords)))
        text_clean.append(text.sub("",i))
        
    def text_cleaning(text, stopwords=skl_stopwords):
        panc = string.punctuation + '–'+ '‘'+ '’'+ '“'+'”'
        text = [i for i in text if not re.findall("[^\u0000-\u05C0\u2100-\u214F]+",i)]
        text = ''.join([ch for ch in text if ch not in panc]) #remove punctuation
        text = re.sub(pattern= '[0-9]+', string= text, repl = ' ' )
        text = re.sub(pattern= '\s', string= text, repl = ' ' )
        text = re.sub(pattern = '(aah|aaaa|aa)', string = text, repl ='')
        text = re.sub(pattern = '\#\S+', string = text, repl ='') # removes hastags
        text = re.sub(pattern = '(\#|@|http\S+|[0-9]|"|)',string = text, repl ='') #removes url, #,@,space, numbers
        return text
    
    s = SentimentIntensityAnalyzer() #initializing the model
    global sentiment_df
    sentiment_df = pd.DataFrame() #initializin the dataframe to store the sentiments
    for i,lst in enumerate(text_clean):#sample_lst
        text = text_cleaning(lst,stopwords=skl_stopwords) #textcleaning
        score = s.polarity_scores(text) #calculating sentiment
        score['tweet'] = text #updating the output of sentiment analysis with the respective tweet
        sentiment_df = sentiment_df.append(score,ignore_index = True) # updating the dataframe with results (Sentiments)
    sentiment_df.reindex(columns=['tweet','neg','neu','pos','compound']) #reindexing the column 
    

    Sentiment_label = []
    for i, row in sentiment_df.iterrows():
        if (row['compound'] > 0.5):
            Sentiment_label.append('Positive')
        elif (row['compound'] >= -0.5 and row['compound'] <= 0.5):
            Sentiment_label.append('Neutral')
        else:
            Sentiment_label.append('Negative')
    sentiment_df['Sentiment_label'] = Sentiment_label
    #print(sentiment_df)
        
    
    sns.countplot(data = sentiment_df, x  =sentiment_df['Sentiment_label'])
   
    # word cloud
    labels = ['Positive','Negative','Neutral']#'Highly Positive','Highly Negative'
    for i, label in enumerate(labels):
        i = i+1
        print('-'*110)
        print(i,'.','#'*30,label,'#'*30)
        print('-'*110)
        senti_labels = sentiment_df[sentiment_df['Sentiment_label'] == label]
        #print(sneti_labels)
        wordCloud = WordCloud(
                background_color="black", 
                width=1600, 
                height=800,
                stopwords=skl_stopwords).generate(' '.join(senti_labels.tweet))

        plt.figure(figsize=(15,10), facecolor='k')
        plt.imshow(wordCloud,interpolation="bilinear")
        plt.axis("off")
        plt.show()
        
            
#transform(sample_lst)

def load(dataframe):
    dataframe.to_sql('doge_table', pg, if_exists='replace')
#load(sentiment_df)


#calling functions:
extract("tweetcollector","Dogecoin_test")
transform(sample_lst)
load(sentiment_df)

