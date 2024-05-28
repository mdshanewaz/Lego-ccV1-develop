import json
import logging
import os
from typing import Dict

import numpy as np
import pandas as pd
from elasticsearch import Elasticsearch

logging.basicConfig(filename="es.log", level=logging.INFO)

ES_HOSTS 	= [""]
ES_PORT 	= ""
ES_USERNAME = os.environ["ES_ACCESS_KEY"]
ES_PASSWORD = os.environ["ES_ACCESS_SECRET"]

class EsManagement:
    def __init__(self):
        self.es_client = Elasticsearch(ES_HOSTS, http_auth=(ES_USERNAME, ES_PASSWORD))
        logging.info(self.es_client.ping())

    def create_index(self, index_name: str, mapping: Dict) -> None:
        """
        Create an ES index.
        :param index_name: Name of the index.
        :param mapping: Mapping of the index
        """
        index_name = ""
        mapping = ""
        logging.info(f"Creating index {index_name} with the following schema: {json.dumps(mapping, indent=2)}")
        self.es_client.indices.create(index=index_name, ignore=400, body=mapping)

    def populate_index(self, path: str, index_name: str) -> None:
        """
        Populate an index from a CSV file.
        :param path: The path to the CSV file.
        :param index_name: Name of the index to which documents should be written.
        """
        path = ""
        index_name = ""
        df = pd.read_csv(path).replace({np.nan: None})
        logging.info(f"Writing {len(df.index)} documents to ES index {index_name}")
        for doc in df.apply(lambda x: x.to_dict(), axis=1):
            self.es_client.index(index=index_name, body=json.dumps(doc))
