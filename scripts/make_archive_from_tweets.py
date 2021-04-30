#!/usr/bin/env python3
import json

import pandas as pd

from nltk.tokenize import TweetTokenizer


def main():
    df = pd.read_csv("../tweets/tweets.csv", sep=",", encoding="UTF-8")
    docs = []
    tokenizer = TweetTokenizer()
    for text in df["Tweet_Text"]:
        try:
            toks = tokenizer.tokenize(text)
            docs.append(toks)
        except:
            print(text)

    with open("../tweets/tweets.json", "w") as file:
        json.dump(docs, file, indent=4)


if __name__ == "__main__":
    main()
