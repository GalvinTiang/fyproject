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

url = "https://raw.githubusercontent.com/GalvinTiang/datamanagementfyp/master/price/priceVSOLAR.csv"

data = pd.read_csv(url, sep=";")

data.to_sql(con=engine, name='priceVSOLAR', index= False, if_exists='replace')