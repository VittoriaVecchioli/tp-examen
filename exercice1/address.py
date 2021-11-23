import requests
import os
from dotenv import load_dotenv
from elasticsearch import Elasticsearch

load_dotenv()

ES_URL = os.environ["ES_URL"]
INDEX = os.environ["ES_INDEX"]

url = "https://api-adresse.data.gouv.fr/search"



adresses = ["8+bd+du+port", "12+rue+emil+renaud", "5+rue+thomas+edison", "12+rue+marechal+ney"]


for adresse in adresses:
     params = {"q": adresse}
     res = requests.get(url, params = params)
     for record in res.json()["features"]:
         print(record["properties"])
         id = int(record["properties"]["postcode"])
         requests.post(f"{ES_URL}/{INDEX}-2021-11-23/_doc/{id}", json = {"id":id, "data":record})

requests.post(f"{ES_URL}/_aliases",json=
    {
        "actions":
            [
                {
                    "add":
                        {
                            "index": f"{INDEX}-2021-11-23",
                            "alias":f"{INDEX}"
                        }
                }
            ]
    },
    verify=False,
)

# see if load done with success
es = Elasticsearch(hosts = [ES_URL], verify=False)
print(es.ping())
res = es.search(index = INDEX, body={"query":{"term": {"id":{"value":72000}}}})
print(res)