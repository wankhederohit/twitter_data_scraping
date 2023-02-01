import snscrape.modules.twitter as snstwitter
import pandas as pd
import streamlit as st

st.title('Twitter Data Scrapping ')
tweet_data = []
search_keyword = st.text_input('Enter a Keyword to Search')
numbers = st.slider('select a range to search', 0, 100)
for i, tweet in enumerate(snstwitter.TwitterSearchScraper('{}'.format(search_keyword)).get_items()):
    if i > numbers:
        break
    tweet_data.append([tweet.date, tweet.id, tweet.url, tweet.content, tweet.user.username,
                       tweet.lang, tweet.source, tweet.retweetCount, tweet.replyCount, tweet.likeCount])

df = pd.DataFrame(tweet_data, columns=['date', 'id', 'url', 'content', 'username', 'lang', 'source', 'retweet_count', 'reply_count', 'like_count'])
st.dataframe(df)
text_contents = df.to_json()
st.download_button(label="Download data in json file",
    data = text_contents,
    file_name = 'data_file'
)
