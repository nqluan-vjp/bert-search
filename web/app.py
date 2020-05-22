import os
import sys
import logging
import codecs
from pprint import pprint
from pyknp import Juman
from flask import Flask, render_template, jsonify, request
from elasticsearch import Elasticsearch
from bert_serving.client import BertClient
SEARCH_SIZE = 10
INDEX_NAME = 'db_medical'
app = Flask(__name__)
logging.basicConfig(level=logging.ERROR)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search')
def analyzer():
    bc = BertClient(ip='bertserving', output_fmt='list')
    client = Elasticsearch('elasticsearch:9200')
    texts = []
    jumanpp = Juman()
    query = request.args.get('q')
    result = jumanpp.analysis(query)
    for mrph in result.mrph_list():
        texts.append(mrph.midasi)
    query_vector = bc.encode([texts],is_tokenized=True)[0]
    app.logger.error(texts)
    script_query = {
        "script_score": {
            "query": {"match": {"source": "tb"}},
            "script": {
                "source": "cosineSimilarity(params.query_vector, doc['question_vector']) + 1.0",
                "params": {"query_vector": query_vector}
            }
        }
    }

    response = client.search(
        index=INDEX_NAME,
        body={

           "size": SEARCH_SIZE,
            "query": script_query
        }
    )
    return jsonify(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
