#!/usr/bin/env python3
import json

import pandas as pd


def main():
    df = pd.read_csv("../tweets/tweets.csv", sep=",", encoding="UTF-8")
    docs = []
    for text in df["Tweet_Text"]:
        docs.append(text)

    with open("../tweets/tweets.json", "w") as file:
        json.dump(docs, file, indent=4)


if __name__ == "__main__":
    main()
