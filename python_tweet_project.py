import os
import pandas as pd
from pandas.core.frame import DataFrame
import tweepy as tw
import datetime 
import csv
pd.set_option("display.precision", 2)

consumer_key = os.environ.get('C_KEY')
consumer_secret = os.environ.get('C_SECRET')
access_token = os.environ.get('A_TOKEN')
access_token_secret = os.environ.get('A_TOKEN_SECRET')

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)

print("start")
try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")

# Define the search terms
search_words = "#Latvija"
language = "lv"
date_until = datetime.date.today()
item_count = 50

# Collect tweets
tweets = tw.Cursor(api.search_tweets,
              q = search_words,
              lang = language,
              until = date_until).items(item_count)
                  
# Open a file to append data to
file_path = '/Users/ivetanagle/PythonFiles/Python_tweet_project/result.csv'
csvFile = open(file_path, 'w')

#Use csv writer
csvWriter = csv.writer(csvFile)

# Iterate, write a row to the CSV file, print tweets
my_list_of_tweets = []
for tweet in tweets:
    csvWriter.writerow([tweet.created_at, tweet.text, tweet.entities['hashtags'],tweet.user.location, tweet.user.name, 
                        tweet.user.followers_count, tweet.user.statuses_count])
    my_list_of_tweets.append(tweet)
csvFile.close()

# Create a pandas dataframe
header_list = ["Created at", "Text", "Hashtags", "Location","Username", "Followers", "Totaltweets"]
my_df = pd.read_csv(file_path, names=header_list)

print(my_df.info())
print(my_df)

def remove_retweets(df: DataFrame):
    rows_to_drop = df[df['Text'].str.startswith('RT @')]
    return df.drop(df[df['Text'].str.startswith('RT @')].index, inplace = True)

remove_retweets(my_df)

print(my_df)
     






