import pandas as pd
import numpy as np

df_tweets = pd.read_csv("../tweets/tweets.csv", encoding="UTF-8", sep=",")

df_ftd = pd.DataFrame()

df_ftd["Tweet_Text"] = df_tweets["Tweet_Text"]

word_list = {}

for tweet in df_tweets["Tweet_Text"]:
    for word in tweet.split():
        if word not in word_list:
            word_list[word] = 0
        else:
            word_list[word] += 1

for word in word_list.keys():
    counts = np.zeros((1, len(df_tweets)))[0]
    for tweet, count in zip(df_tweets["Tweet_Text"], counts):
        txt = tweet.split()
        for tweet_word in txt:
            if tweet_word == word:
                count += 1
    df_ftd[word] = counts

df_ftd.to_csv("../ftd.csv", encoding="UTF-8", sep=",")