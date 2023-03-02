
import snscrape.modules.twitter as snstwitter
import pandas as pd
from datetime import date
import streamlit as st
from pymongo import MongoClient

st.title('Twitter Data Scrapping ')
tweet_data = []

search_keyword = st.text_input('Enter a Keyword to Search')
numbers = st.slider('select a range to search', 0, 100)
start_date= st.date_input(
    "select start date",
    date(2015, 7, 6))
end_date = st.date_input(
    "select end date",
    date(2022, 7, 6))

for i, tweet in enumerate(snstwitter.TwitterSearchScraper(f'{search_keyword} since:{start_date} until:{end_date}').get_items()):
    if i > numbers:
        break
    tweet_data.append([tweet.date, tweet.id, tweet.url, tweet.content, tweet.user.username,
                       tweet.lang, tweet.source, tweet.retweetCount, tweet.replyCount, tweet.likeCount])

df = pd.DataFrame(tweet_data, columns=['date', 'id', 'url', 'content', 'username', 'lang', 'source', 'retweet_count', 'reply_count', 'like_count'])
st.dataframe(df)
jason_file = df.to_json()
st.download_button(label="Download data in json file",
                   data=jason_file,
                   file_name='data_jason_file')

csv_file = df.to_csv()
st.download_button(label="Download data in csv file",
                   data=csv_file,
                   file_name='data_csv_file')


client = MongoClient('mongodb://127.0.0.1:27017/')
mydb= client['Twitter_Scrapped_Data']
data = mydb.scrapped_data
filtered_data = [{'Keyword': search_keyword,
                  'startdate': str(start_date),
                  'enddate': str(end_date),
                  'data': tweet_data
                  }]

data.insert_many(filtered_data)