# bert-sample

## Getting Started

### 1. Download a pretrained BERT model


```bash
$ wget http://nlp.ist.i.kyoto-u.ac.jp/DLcounter/lime.cgi?down=http://nlp.ist.i.kyoto-u.ac.jp/nl-resource/JapaneseBertPretrainedModel/Japanese_L-12_H-768_A-12_E-30_BPE.zip&amp;name=Japanese_L-12_H-768_A-12_E-30_BPE.zip
$ mv lime.cgi?down=http:%2F%2Fnlp.ist.i.kyoto-u.ac.jp%2Fnl-resource%2FJapaneseBertPretrainedModel%2FJapanese_L-12_H-768_A-12_E-30_BPE.zip Japanese_L-12_H-768_A-12_E-30_BPE.zip
$ unzip Japanese_L-12_H-768_A-12_E-30_BPE.zip
```


### 2. Clone source code 

```bash
$ git clone https://github.com/nqluan-vjp/bert-search.git
```


### 3. Set environment variables 

Set a pretrained BERT model and Elasticsearch's index name as environment variables:
 
```bash
$ cd bert-search
$ nano .env
```

Copy content below to file .env

```bash
$ PATH_MODEL=./Japanese_L-12_H-768_A-12_E-30_BPE
$ INDEX_NAME=jobsearch
```

### 4. Run Docker containers


```bash
$ cd bert-search
$ docker-compose up
```


### 5. Create index

```bash
$ cd bert-search\example
$ python create_index.py --index_file=index.json --index_name=jobsearch
# index.json
{
  "settings": {
    "number_of_shards": 2,
    "number_of_replicas": 1
  },
  "mappings": {
    "dynamic": "true",
    "_source": {
      "enabled": "true"
    },
    "properties": {
      "title": {
        "type": "text"
      },
      "text": {
        "type": "text"
      },
      "text_vector": {
        "type": "dense_vector",
        "dims": 768
      }
    }
  }
}
```


### 6. Create documents

Once you created an index, you’re ready to index some document.

```bash
$ python create_documents.py --data=example.csv --index_name=jobsearch
# example/example.csv
```

After finishing the script, you can get a JSON document like follows:

```python
# documents.jsonl
```

### 7. Index documents

After converting data into a JSON, adds a JSON document to the specified index and makes it searchable.

```bash
$ python example/index_documents.py
```

### 8. Open browser

Go to <http://127.0.0.1:5000>.