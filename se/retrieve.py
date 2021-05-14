def retrieve(index, query):
    try:
        index_query = query.evaluate(index)
        return index_query
    except:
        return set()
