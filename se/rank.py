import re


def score_document(query, doc):
    score = 0
    for word in doc:
        if word in query:
            score += 1
    return score


def rank_documents(query, docs, index_query):
    ranked_index = []
    for doc_number in index_query:
        if doc_number != "idf":
            num = int(re.sub(r"doc_(\d+)", r"\1", doc_number))
            doc = docs[num]
            score = score_document(query, doc)
            ranked_index.append((score, num))
    ranked_index = sorted(ranked_index, key=lambda x: -x[0])
    return [item[1] for item in ranked_index]
