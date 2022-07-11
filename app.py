from cgitb import handler
from logging import handlers
import numbers
from flask import Flask, flash, render_template, session, redirect, request, Response
from flask_sqlalchemy import SQLAlchemy
import pymysql
import pandas as pd
import os, re, string, natsort, nltk
import matplotlib
import numpy as np
from textblob import TextBlob
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io, base64
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3307/stock'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '#$%^'
csrf.init_app(app)
db = SQLAlchemy(app)

datab = pymysql.connect(
    host="localhost", 
    user="root",
    password= "root",
    database= "stock",
    port= 3307
)

class SearchForm(FlaskForm):
    stock = StringField(label=('Stock Name'))
    submit = SubmitField(label=('Submit'))

@app.route('/' , methods=['GET','POST'])
def index():
    form = SearchForm()
    error = None
    if form.validate_on_submit():
        try:
            formvalue = str({form.stock.data})
            query = formvalue.translate(str.maketrans('', '', string.punctuation))
            sql = "SELECT * FROM stock." + str(query)
            sql2 = "SELECT * FROM stock.price" +  str(query)
            df = pd.read_sql_query(sql,datab)
            df2 = pd.read_sql_query(sql2,datab)

            columns_name = ['date', 'polarity', 'subjectivity', 'sentiment']
            df.columns = columns_name
            df['date'] = pd.to_datetime(df['date'])
            df['quarter'] = df['date'].dt.to_period('Q')
            df.quarter = df.quarter.astype(str)

            quarters = df["quarter"].unique().tolist()
            sentiments = df["sentiment"].unique().tolist()
            sentiments_dict = {}
            for sent in sentiments:
                sentiments_dict[sent] = []
            for quart in quarters:
                sent_counts = df.loc[df["quarter"] == quart, "sentiment"].value_counts()
                for sent in sentiments:
                    if sent in sent_counts.index.tolist():
                        count = sent_counts[sent]
                    else:
                        count = 0
                    sentiments_dict[sent].append(count)

            sentiment_count_df = pd.DataFrame(sentiments_dict)
            sentiment_count_df.insert(loc = 0, column ="year_quarter", value = quarters)

            x = np.arange(0,len(sentiment_count_df),1)
            fig, ax1 = plt.subplots(1,1)
            ax1.plot(x, sentiment_count_df['Neutral'])
            ax1.set_xticks(x)
            ax1.set_xticklabels(sentiment_count_df['year_quarter'])

            ax2 = ax1.twinx()
            ax2.plot(sentiment_count_df['year_quarter'],sentiment_count_df['Positive'],color='blue')

            ax3 = ax1.twinx()
            ax3.plot(sentiment_count_df['year_quarter'],sentiment_count_df['Negative'],color='red')

            ax4 = ax1.twinx()
            ax4.plot(sentiment_count_df['year_quarter'],df2['price'],color='purple')

            ax1.set_ylabel('Number of Sentiments')
            ax4.set_ylabel('Price')
            ax1.set_xlabel('Year Quarter')

            ax1.tick_params(axis='y',color='green')
            ax2.tick_params(axis='y',color='blue')
            ax3.tick_params(axis='y',color='red')
            ax4.tick_params(axis='y',color='purple')
            ax1.tick_params(axis='x',which='major', labelsize=5)

            ax4.spines['right'].set_color('purple')

            ax3.set_title(query)

            ax2.get_yaxis().set_visible(False)
            ax3.get_yaxis().set_visible(False)

            green_patch = mpatches.Patch(color='green', label='Neutral')
            blue_patch = mpatches.Patch(color='blue', label='Positive')
            red_patch = mpatches.Patch(color='red', label='Negative')
            purple_patch = mpatches.Patch(color='purple',label='Price')

            plt.legend(handles=[green_patch,blue_patch,red_patch,purple_patch])

            pngImage = io.BytesIO()
            plt.savefig(pngImage, format='png')
            pngImage.seek(0)
            plot_url = base64.b64encode(pngImage.getvalue()).decode('utf8')

            pngImageB64String = "data:image/png;base64,"
            pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
            return render_template('image.html', form=form, query = query, plot_url = plot_url)
        except Exception as e:
            if formvalue == "" :
                flash("Please Enter A Stock!!!")
            else:
                flash("Invalid Stock is entered!!!")    
    return render_template('image.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)


    flash('Please enter a stock.')