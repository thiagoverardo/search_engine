def retrieve(index, query):
    index_query = set(index[query[0]])
    for q in query[1:]:
        index_query &= set(index[q])
    return index_query