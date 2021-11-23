import uvicorn
from dotenv import load_dotenv
import os

from app import create_app

if __name__== "__main__":
    load_dotenv()
    api_port = int(os.environ["API_PORT"])
    api_host = os.environ["API_HOST"]
    elastic_host = os.environ["ES_URL"]
    elastic_index = os.environ["ES_INDEX"]
    app = create_app(elastic_host, elastic_index)
    print("run api ...")
    uvicorn.run(app, host=api_host, port=api_port)
