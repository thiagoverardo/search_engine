def retrieve(index, query):
    if len(query) == 2:
        index_query = set(index[query[1]])
    elif len(query) > 2:
        index_query = set(index[query[1][-1]])
    if len(query) > 2:
        for query_term in query[2:]:
            if query[0] == "and":
                if query_term[0] == "term":
                    index_query &= set(index[query_term[-1]])
                else:
                    index_query &= retrieve(index, query_term)
            elif query[0] == "or":
                if query_term[0] == "term":
                    index_query |= set(index[query_term[-1]])
                else:
                    index_query |= retrieve(index, query_term)
    return index_query
