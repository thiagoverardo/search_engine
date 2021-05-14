import re
from se.index import load_index
from se.query import Term


def get_terms(query):
    terms = []
    if type(query) == type(Term("teste")):
        return query.term
    else:
        for node in query.nodes:
            terms.append(get_terms(node))
        return terms


def score_document(query, doc, doc_num):
    words = get_terms(query)
    score = 0
    index = load_index("../index.json")
    for word in doc.split():
        if word.lower() in words:
            score += index[word.lower()][f"doc_{doc_num}"]["tf-idf"]
    return score


def rank_documents(query, docs, index_query):
    ranked_index = []
    for doc_number in index_query:
        if doc_number != "idf":
            num = int(re.sub(r"doc_(\d+)", r"\1", doc_number))
            doc = docs[num]
            score = score_document(query, doc, num)
            ranked_index.append((score, num))
    ranked_index = sorted(ranked_index, key=lambda x: -x[0])
    return [item[1] for item in ranked_index]
