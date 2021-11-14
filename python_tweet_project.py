import os
import pandas as pd
from pandas.core.frame import DataFrame
import tweepy as tw
import datetime 
from email.utils import parsedate_tz, mktime_tz
import csv

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 900)

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
item_count = 100

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

#Change date format
my_df['Created at'] = my_df['Created at'].map(lambda x: x.rstrip('+00:00'))

print(my_df.info())
print("Original dataframe: \n")
print(my_df[['Created at', 'Text', 'Hashtags', 'Username']].head(10))


# Remove retweets from df
def remove_retweets(df: DataFrame):
    rows_to_drop = df[df['Text'].str.startswith('RT @')]
    return df.drop(df[df['Text'].str.startswith('RT @')].index)

cleaned_df = remove_retweets(my_df)
print("Cleaned dataframe without retweets: \n")
print(cleaned_df[['Created at', 'Text', 'Hashtags', 'Username']].head(10))

# Get info about users
def get_info(df, id):
    return df.loc[id, :]

#Find most popular user by number of followers
most_popular_user = cleaned_df['Followers'].idxmax()
print(f"\n Detailed info about the most popular tweeter(by number of followers): \n {get_info(cleaned_df, most_popular_user)}\n ")








