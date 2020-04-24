"""
Example script to create elasticsearch documents.
"""
import argparse
import json
import os

import pandas as pd
from bert_serving.client import BertClient
bc = BertClient(ip='127.0.0.1', port=5555, port_out=5556,output_fmt='list')


def create_document(doc, emb, index_name):
    return {
        '_op_type': 'index',
        '_index': index_name,
        'id': doc['id'],
        'source': doc['source'],
        'question': doc['question'],
        'page': doc['page'],
        'category': doc['category'],
        'generic': doc['generic'],
        'applicant': doc['applicant'],
        'issue_date': doc['issue_date'],
        'r_issue_date': doc['r_issue_date'],
        'molecular_weight': doc['molecular_weight'],
        'modality': doc['modality'],
        'adaptive_disease': doc['adaptive_disease'],
        'adm_route': doc['adm_route'],
        'doc_id': doc['doc_id'],
        'question_vector': emb
    }


def load_dataset(path):
    files = []
    docs = []
    for r, d, f in os.walk(path):
        for file in f:
            if '.json' in file:
                files.append(os.path.join(r, file))
    for f in files:
        with open(f, 'r',encoding="utf-8_sig") as myfile:
            data=myfile.read()
            print(data)
        obj = json.loads(data)
        for item in obj: 
                doc = {
                    'id': item['id'],
                    'source': item['source'],
                    'question': item['question'],
                    'page': item['page'],
                    'category': item['category'],
                    'generic': item['generic'],
                    'applicant': item['applicant'],
                    'issue_date': item['issue_date'],
                    'r_issue_date': item['r_issue_date'],
                    'molecular_weight': item['molecular_weight'],
                    'modality': item['modality'],
                    'adaptive_disease': item['adaptive_disease'],
                    'adm_route': item['adm_route'],
                    'doc_id': item['doc_id'],
                }
                docs.append(doc)
    return docs


def bulk_predict(docs, batch_size=256):
    """Predict bert embeddings."""
    for i in range(0, len(docs), batch_size):
        batch_docs = docs[i: i+batch_size]
        embeddings = bc.encode([doc['question'] for doc in batch_docs])
        for emb in embeddings:
            yield emb


def main(args):
    docs = load_dataset(args.data)
    with open(args.save, 'w', encoding="utf-8") as f:
        for doc, emb in zip(docs, bulk_predict(docs)):
            d = create_document(doc, emb, args.index_name)
            f.write(json.dumps(d, ensure_ascii=False) + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Creating elasticsearch documents.')
    parser.add_argument('--data', help='data for creating documents.')
    parser.add_argument('--save', default='documents.jsonl', help='created documents.')
    parser.add_argument('--index_name', default='jobsearch', help='Elasticsearch index name.')
    args = parser.parse_args()
    main(args)
