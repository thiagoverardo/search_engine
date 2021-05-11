def retrieve(index, query):
    print(query)
    index_query = set(index[query[0]])
    for query_term in query[1:]:
        index_query &= set(index[query_term])
    return index_query
