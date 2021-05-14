#!/usr/bin/env python3
from argparse import ArgumentParser

from se.archive import load_archive
from se.index import load_index
from se.search import search

from pysinonimos.sinonimos import Search, historic


MSG_DESCRIPTION = "Busca."


def main():
    parser = ArgumentParser(description=MSG_DESCRIPTION)
    parser.add_argument("filename_docs", help="Os doc.")
    parser.add_argument("filename_index", help="Os indice.")
    parser.add_argument("query", nargs="+", help="A query.")
    args = parser.parse_args()

    docs = load_archive(args.filename_docs)
    index = load_index(args.filename_index)

    nro = 0
    for e in args.query:
        if e != "or" and e != "and":
            sinArg = Search(e)
            sinArg = sinArg.synonyms()
            args.query[nro] = [args.query[nro]]
            if sinArg != 404:
                for i in sinArg: 
                    args.query[nro].append("or")
                    args.query[nro].append(i)
                " ".join(args.query[nro])
        nro += 1

    nro = 0
    argsfinal = ""
    for e in args.query:
        if e != "or" and e != "and":
            argsfinal += " ".join(args.query[nro])
        else:
            argsfinal += f" {args.query[nro]} "
        nro += 1

    docs_searched = search(argsfinal, index, docs)

    for doc in docs_searched:
        print("".join(doc))
        print("=" * 80)


if __name__ == "__main__":
    main()
