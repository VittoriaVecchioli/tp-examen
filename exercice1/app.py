import os
from fastapi import FastAPI, HTTPException
from elasticsearch import Elasticsearch

def create_app(elastic_host, elastic_index):
    print("starting api ...")
    app = FastAPI(title="Exposition API adresse postale")
    print("connect to elastic cluster ...")
    es = Elasticsearch(hosts = elastic_host, verify=False)
    print("define queries ...")
    @app.get("/postcode/{postcode}",summary="get information by postcode")
    def get_postcode(postcode):
        res = es.search(index = elastic_index, body={"query":{"term": {"id":{"value":int(postcode)}}}})
        print(res)
        if len(res["hits"]["hits"])==0:
            raise HTTPException(status_code=404, detail="postcode information not found")
        else :
            return res["hits"]["hits"]
    return app