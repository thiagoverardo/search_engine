#!/usr/bin/env python3
import json
import numpy as np
from collections import defaultdict


def load_archive(path):
    with open(path, "r") as file:
        return json.load(file)


def make_index(docs):
    N = len(docs)
    index = defaultdict(list)
    for k, doc in enumerate(docs):
        name = f"doc_{k}"
        for word in doc:
            if word in index:
                if name in index[word]:
                    index[word][name]["ftd"] += 1
                else:
                    index[word][name] = {"ftd": 1}
            else:
                index[word] = {name: {"ftd": 1}, "idf": 0}
            index[word][name]["tftd"] = np.log(1 + index[word][name]["ftd"])
            nt = len(index[word]) - 1
            index[word]["idf"] = np.log(N / nt)

    for word in index:
        for doc in index[word]:
            if doc != "idf":
                index[word][doc]["tf-idf"] = (
                    index[word]["idf"] * index[word][doc]["tftd"]
                )
    return index


def save_index(index, path):
    with open(path, "w") as file:
        json.dump(index, file, indent=4)


def main():

    docs = load_archive("../tweets/tweets.json")
    index = make_index(docs)

    save_index(index, "../index.json")


if __name__ == "__main__":
    main()
