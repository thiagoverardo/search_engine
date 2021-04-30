from dotenv import load_dotenv
import pandas as pd
import tweepy as tp
import os
import re

load_dotenv(verbose=True)

auth = tp.AppAuthHandler(os.getenv("ACCESS_KEY"), os.getenv("SECRET_KEY"))

api = tp.API(auth)

tweets = api.user_timeline(
    screen_name="LucianoHuck",
    # 200 is the maximum allowed count
    count=200,
    include_rts=False,
    exclude_replies=True,
    # Necessary to keep full_text
    # otherwise only the first 140 words are extracted
    tweet_mode="extended",
)

all_tweets = []
oldest_id = tweets[-1].id
for tweet in tweets:
    all_tweets.append(tweet.full_text.replace("\n", " "))

while True:
    tweets = api.user_timeline(
        screen_name="LucianoHuck",
        # 200 is the maximum allowed count
        count=200,
        include_rts=False,
        max_id=oldest_id - 1,
        # Necessary to keep full_text
        # otherwise only the first 140 words are extracted
        tweet_mode="extended",
    )
    if len(tweets) == 0:
        break
    oldest_id = tweets[-1].id
    for tweet in tweets:
        all_tweets.append(tweet.full_text.replace("\n", " "))
    print("N of tweets downloaded till now {}".format(len(all_tweets)))

df = pd.DataFrame(columns=["Tweet_Text"], data=all_tweets)

url_expression = "(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?"
punctuation = r"[\.\,\!\:\;\'\"\\\|\/\>\<\?\(\)\[\]\}\{]"

df["Tweet_Text"] = df["Tweet_Text"].str.lower()
df["Tweet_Text"] = df["Tweet_Text"].str.replace(url_expression, "", regex=True)
df["Tweet_Text"] = df["Tweet_Text"].str.replace(r"\s\-\s|\-\-+", " ", regex=True)
df["Tweet_Text"] = df["Tweet_Text"].str.replace(punctuation, " ", regex=True)

df = df[df["Tweet_Text"].str.replace(" ", "") != ""]

df.to_csv("tweets/tweets.csv", encoding="UTF-8", sep=",")