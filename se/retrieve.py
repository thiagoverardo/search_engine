def retrieve(index, query):
    index_query = query.evaluate(index)
    return index_query