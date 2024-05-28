from es_connection import EsManagement

es_connection = EsManagement()

# Querying data
# Query and filter contexts
query = {
    "query": {
        "bool": {
            "must": [
                {"match": {"type": "TV Show"}},
            ],
            "filter": [
                {"range": {"release_year": {"gte": 2021}}}
            ]
        }
    }
}

results = es_connection.es_client.search(index="netflix_movies", body=query)

# Result
print([i["_source"]["title"] for i in results["hits"]["hits"]])
