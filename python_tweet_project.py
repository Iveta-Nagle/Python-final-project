import os
import pandas as pd
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
search_words = "#lokdauns"
language = "lv"
date_until = datetime.date.today()
item_count = 15

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
    csvWriter.writerow([tweet.created_at, tweet.user.name, tweet.user.location, tweet.text])
    print (tweet.created_at)
    print (tweet.user.name)
    print (tweet.user.location)
    print (tweet.text + '\n')
    my_list_of_tweets.append(tweet)
csvFile.close()

# Create a pandas dataframe
header_list = ["Created at", "Username", "Location", "Text"]
my_df = pd.read_csv(file_path, names=header_list)

print(my_df.info())
print(my_df)


name = 'Haris'
# Number of tweets to pull
tweetCount = 5

# Calling the user_timeline function with our parameters
results = api.user_timeline(screen_name=name, count=tweetCount)

# foreach through all tweets pulled
for tweet in results:
   # printing the text stored inside the tweet object
   print (tweet.text)




