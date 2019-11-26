from flask import current_app

def add_to_index(index, model):
    if not current_app.elasticsearch:
        return
    payload = {}
    for field in model.__searchable__:
        payload[field] = getattr(model, field)
    current_app.elasticsearch.index(index=index, id=model.id, body=payload, doc_type={})

def remove_from_index(index, model):
    if not current_app.elasticsearch:
        return
    current_app.elasticsearch.delete(index=index, id=model.id)

def query_index(index, query, page, per_page):
    if not current_app.elasticsearch:
        return [], 0
    print("from:", (page - 1) * per_page)
    print("size:", per_page)
    search = current_app.elasticsearch.search(
        index=index,
        body={'query': {'multi_match': {'query': query, 'fields': ['*']}},
              'from': (page - 1) * per_page, 'size': per_page})
    print([hit['_id'] for hit in search['hits']['hits']])
    print(type(search['hits']))
    print("hits:", search['hits'])
    print(type(search['hits']['total']))
    print('total:',search['hits']['total'])
    ids = [hit['_id'] for hit in search['hits']['hits']]
    return ids, search['hits']['total']