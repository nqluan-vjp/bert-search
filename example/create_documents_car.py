"""
Example script to create elasticsearch documents.
"""
import argparse
import json
import os

import pandas as pd
from bert_serving.client import BertClient
bc = BertClient(ip='3.112.235.215', port=9555, port_out=9556,output_fmt='list')


def create_document(doc, emb, index_name):
    return {
        '_op_type': 'index',
        '_index': index_name,
        'number': doc['number'],
        'reception_date': doc['reception_date'],
        'gender': doc['gender'],
        'address': doc['address'],
        'declaration_method': doc['declaration_method'],
        'vehicle_name': doc['vehicle_name'],
        'nickname': doc['nickname'],
        'registration_date': doc['registration_date'],
        'total_mileage': doc['total_mileage'],
        'model': doc['model'],
        'prime_mover_model': doc['prime_mover_model'],
        'defective_device': doc['defective_device'],
        'time_of_emergence': doc['time_of_emergence'],
        'summary': doc['summary'],
        'summary_vector': emb
    }


def load_dataset(path):
    docs = []
    df = pd.read_csv(path)
    for row in df.iterrows():
        doc = {
            'number': row[1].番号,
            'reception_date': row[1].受付日,
            'gender': row[1].性別,
            'address': row[1].住所,
            'declaration_method': row[1].申告方法,
            'vehicle_name': row[1].車名,
            'nickname': row[1].通称名,
            'registration_date': row[1].初度登録年月,
            'total_mileage': row[1].総走行距離,
            'model': row[1].型式,
            'prime_mover_model': row[1].原動機型式,
            'defective_device': row[1].不具合装置,
            'time_of_emergence': row[1].発生時期,
            'summary': row[1].申告内容の要約
        }
        docs.append(doc)   
    return docs


def bulk_predict(docs, batch_size=256):
    """Predict bert embeddings."""
    jumanpp = Juman()
    for i in range(0, len(docs), batch_size):
        batch_docs = docs[i: i+batch_size]
        pre_embedding_docs = []
        list_docs = []
        for doc in batch_docs:
            summary = re.sub(r'\s+', '', doc['summary'])
            result = jumanpp.analysis(summary)
            texts = [mrph.midasi for mrph in result.mrph_list()]
            pre_embedding_docs.append(texts)
        list_docs.append(" ".join(pre_embedding_docs))    
        embeddings = bc.encode(list_docs,is_tokenized=False)
        print(pre_embedding_docs)
        for emb in embeddings:
            yield emb

def get_info():
    list = []
    my_list =['私', 'は', 'クリーム', 'パン', 'が', '食べ', 'たい']
    list.append(" ".join(my_list))
    print (list)
    embeddings2 = bc.encode(list, is_tokenized=False, show_tokens = True)
    return embeddings2
    
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
