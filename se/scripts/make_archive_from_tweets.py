import json

from argparse import ArgumentParser

import pandas as pd

from nltk.tokenize import TweetTokenizer

from se.utils import save_archive


MSG_DESCRIPTION = 'Le arquivo de tweets e gera JSON com tweets tokenizados.'


def main():
    parser = ArgumentParser(description=MSG_DESCRIPTION)
    parser.add_argument('filename_tweets', help='Os tweet.')
    parser.add_argument('filename_archive', help='Onde guarda.')
    args = parser.parse_args()

    df = pd.read_csv(args.filename_tweets)
    docs = []
    tokenizer = TweetTokenizer()
    for text in df['Tweet_Text']:
        toks = tokenizer.tokenize(text)
        docs.append(toks)

    save_archive(docs, args.filename_archive)


if __name__ == '__main__':
    main()
