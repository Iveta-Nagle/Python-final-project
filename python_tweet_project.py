import os
import pandas as pd
import tweepy as tw
import datetime 
import csv

print("start")


consumer_key = os.environ.get('C_KEY')
consumer_secret = os.environ.get('C_SECRET')
access_token = os.environ.get('A_TOKEN')
access_token_secret = os.environ.get('A_TOKEN_SECRET')

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)

try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")

# Define the search term
search_words = "#Latvia"
language = "lv"
date_until = datetime.date.today()
item_count = 10

# Collect tweets
tweets = tw.Cursor(api.search_tweets,
              q = search_words,
              lang = language,
              until = date_until).items(item_count)
                  
# Open/create a file to append data to
file_path = '/Users/ivetanagle/PythonFiles/Python_tweet_project/result.csv'
csvFile = open(file_path, 'w')

#Use csv writer
csvWriter = csv.writer(csvFile)

# Iterate, write a row to the CSV file, print tweets
my_list_of_tweets = []
for tweet in tweets:
    csvWriter.writerow([tweet.created_at, tweet.user.name, tweet.text.encode('utf-8')])
    print (tweet.created_at)
    print (tweet.user.name)
    print (tweet.text + '\n')
    my_list_of_tweets.append(tweet)
csvFile.close()

# We create a pandas dataframe as follows:
my_df = pd.DataFrame(data = my_list_of_tweets, 
                    columns = ['created_at'])

print(type(my_list_of_tweets))

# We display the first 10 elements of the dataframe:
print(my_df)


