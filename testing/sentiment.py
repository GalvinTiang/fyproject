import pandas as pd
import mysql.connector as connection
import os
import re
import matplotlib
import string
import nltk
import numpy as np
import natsort
from textblob import TextBlob
import mysql.connector as connection
# IMPORT THE SQALCHEMY LIBRARY's CREATE_ENGINE METHOD
from sqlalchemy import create_engine
import pymysql
  
# DEFINE THE DATABASE CREDENTIALS
host="localhost"
user = 'root'
password = 'root'
port = 3307
database = 'stock'

engine = create_engine("mysql+mysqlconnector://{0}:{1}@{2}:{3}/{4}".format(
            user, password, host, port, database
        ))

columns_name = ['urls_link', 'date', 'urls_data_user', 'comments'] 

url = "https://raw.githubusercontent.com/GalvinTiang/datamanagementfyp/master/Latest%20Data/KOSSAN/kossan1_results.csv"
url1 = "https://raw.githubusercontent.com/GalvinTiang/datamanagementfyp/master/Latest%20Data/KOSSAN/kossan_results_2.csv"

df = pd.read_csv(url)
df1 = pd.read_csv(url1)


frames = [df, df1]

data = pd.concat(frames)
data.dropna(inplace = True)
data.columns = columns_name
nltk.download('punkt')
data.drop('urls_link', axis=1, inplace=True) 
data.drop('urls_data_user', axis=1, inplace=True)

def remove_tweet_special(text):
    # remove tab, new line, ans back slice
    text = text.replace('\\t'," ").replace('\\n'," ").replace('\\u'," ").replace('\\',"")
    # remove non ASCII (emoticon, chinese word, .etc)
    text = text.encode('ascii', 'replace').decode('ascii')
    # remove mention, link, hashtag
    text = ' '.join(re.sub("([@#][A-Za-z0-9]+)|(\w+:\/\/\S+)"," ", text).split())
    # remove incomplete URL
    return text.replace("http://", " ").replace("https://", " ")
                
data['comments'] = data['comments'].apply(remove_tweet_special)

#remove number
def remove_number(text):
    return  re.sub(r"\d+", "", text)

data['comments'] = data['comments'].apply(remove_number)

#remove punctuation
def remove_punctuation(text):
    return text.translate(str.maketrans("","",string.punctuation))

data['comments'] = data['comments'].apply(remove_punctuation)

#remove whitespace leading & trailing
def remove_whitespace_LT(text):
    return text.strip()

data['comments'] = data['comments'].apply(remove_whitespace_LT)

#remove multiple whitespace into single whitespace
def remove_whitespace_multiple(text):
    return re.sub('\s+',' ',text)

data['comments'] = data['comments'].apply(remove_whitespace_multiple)

# remove single char
def remove_singl_char(text):
    return re.sub(r"\b[a-zA-Z]\b", "", text)

data['comments'] = data['comments'].apply(remove_singl_char)

data['date'] = pd.to_datetime(data['date'], format = '%b %d, %Y %I:%M %p')
        
natsort.natsorted(data['date'])

pol =  lambda x: TextBlob(x).sentiment.polarity
sub = lambda x: TextBlob(x).sentiment.subjectivity

data['polarity'] = data['comments'].apply(pol)
data['subjectivity'] = data['comments'].apply(sub)
def sentiment(txt):
    if pol(txt) > 0:
        return 'Positive'
    elif pol(txt) == 0:
        return 'Neutral'
    elif  pol(txt) < 0:
        return 'Negative'
    else:
        return 'Unknown'
                
data['sentiment'] = data['comments'].apply(sentiment)

data.drop('comments', axis=1, inplace=True)

data.to_sql(con=engine, name='KOSSAN', index= False, if_exists='replace')