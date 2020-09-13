from elasticsearch import Elasticsearch
import requests

class ElasticService():

    def __init__(self, host, port, username, password):
        super().__init__()
        requests.packages.urllib3.disable_warnings()
        self.es = Elasticsearch(f"https://{host}:{port}", http_auth=(username, password), verify_certs=False)
        self.es.info()


    def create_index(self, index_name):
        self.es.indices.create(index=index_name, ignore=400)

    def create_doc(self, index_name, id, body):
        self.es.create(index=index_name,id=id, body=body)

    def delete_doc(self, index_name, id):
        self.es.delete(index=index_name,id=id)

