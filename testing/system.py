import pandas as pd
import os
import re
import matplotlib
import string
import nltk
import numpy as np
import natsort
from textblob import TextBlob

folderpath =  "C:\\Users\\User\\Desktop\\School\\Sem5\\Project1\\Latest Data\\"
fold_list = os.listdir(folderpath)
lower_fold_list = fold_list.lower()

columns_name = ['urls_link', 'date', 'urls_data_user', 'comments']

for file in fold_list:
#     filename = file.endswith(".csv")
    try :
        data = pd.read_csv("C:\\Users\\User\\Desktop\\School\\Sem5\\Project1\\Latest Data\\"+ fold_list + "\\" + lower_fold_list+"_results")
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

        


                
    except:
            print("{} cant be read".format(file))

quarter_1_2018 = (data['date'] >= '2018-01') & (data['date'] < '2018-03')
quarter_2_2018 = (data['date'] >= '2018-04') & (data['date'] < '2018-06')
quarter_3_2018 = (data['date'] >= '2018-07') & (data['date'] < '2018-09')
quarter_4_2018 = (data['date'] >= '2018-10') & (data['date'] < '2018-12')
quarter_1_2019 = (data['date'] >= '2019-01') & (data['date'] < '2019-03')
quarter_2_2019 = (data['date'] >= '2019-04') & (data['date'] < '2019-06')
quarter_3_2019 = (data['date'] >= '2019-07') & (data['date'] < '2019-09')
quarter_4_2019 = (data['date'] >= '2019-10') & (data['date'] < '2019-12')
quarter_1_2020 = (data['date'] >= '2020-01') & (data['date'] < '2020-03')
quarter_3_2020 = (data['date'] >= '2020-07') & (data['date'] < '2020-09')
quarter_4_2020 = (data['date'] >= '2020-10') & (data['date'] < '2020-12')
quarter_1_2021 = (data['date'] >= '2021-01') & (data['date'] < '2021-03')
quarter_2_2021 = (data['date'] >= '2021-04') & (data['date'] < '2021-06')
quarter_3_2021 = (data['date'] >= '2021-07') & (data['date'] < '2021-09')
quarter_4_2021 = (data['date'] >= '2021-10') & (data['date'] < '2021-12')