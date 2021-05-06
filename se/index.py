import json

from collections import defaultdict
from se.normalization import normalize_text

def make_index(docs):
    index = defaultdict(list)
    for k, doc in enumerate(docs):
        words = set(doc)
        for word in words:
            word = normalize_text(word)
            index[word].append(k)
    return index


def save_index(index, path):
    with open(path, 'w') as file:
        json.dump(index, file, indent=4)


def load_index(path):
    with open(path, 'r') as file:
        return json.load(file)
