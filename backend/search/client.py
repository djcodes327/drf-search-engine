from algoliasearch_django import algolia_engine


def get_client():
    return algolia_engine.client


def get_index(index_name='dj_Product'):
    client = get_client()
    index = client.init_index(index_name)
    return index


def perform_search(query, **kwargs):
    """
    perform_search("hello world", tags=["cars"], public=True)
    here -> "hello world" is our query
    -> tags -> "cars" are tags we are passing
    -> public -> True are for faceting.
    """
    index = get_index()
    params = {}
    tags = ""
    if "tags" in kwargs:
        tags = kwargs.pop("tags") or []
        if len(tags) != 0:
            params["tagFilters"] = tags
    index_filter = [f"{k}:{v}" for k, v in kwargs.items() if v]
    if len(index_filter) != 0:
        params["facetFilters"] = index_filter
    results = index.search(query, params)
    return results
