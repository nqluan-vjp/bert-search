# bert-sample

## Getting Started

### 1. Download a pretrained BERT model


```bash
$ wget http://nlp.ist.i.kyoto-u.ac.jp/nl-resource/JapaneseBertPretrainedModel/Japanese_L-12_H-768_A-12_E-30_BPE.zip
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


### 5. JUMAN++のインストール 


```bash
$ wget https://github.com/ku-nlp/jumanpp/releases/download/v2.0.0-rc2/jumanpp-2.0.0-rc2.tar.xz && \
$ tar xvf jumanpp-2.0.0-rc2.tar.xz && \
$ apt update -y && \ 
$ apt upgrade -y && \ 
$ apt install build-essential -y && \ 
$ apt install cmake -y && \
$ cd jumanpp-2.0.0-rc2 && \ 
$ mkdir build && \ 
$ cd build && \ 
$ cmake .. -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/usr/local && \ 
$ make && \ 
$ make install
```

### 6. KNPのインストール


```bash
$ wget -O knp-4.20.tar.bz2 http://nlp.ist.i.kyoto-u.ac.jp/nl-resource/knp/knp-4.20.tar.bz2
$ tar jxvf knp-4.20.tar.bz2
$ cd knp-4.20
$ ./configure
$ make
$ sudo make install
```


### 7. Create index

```bash
$ cd bert-search\example
$ python create_index.py --index_file=index.json --index_name=INDEX_NAME
# index.json
{
  "settings": {
    "number_of_shards": 14,
    "number_of_replicas": 1
  },
  "mappings": {
    "dynamic": "true",
    "_source": {
      "enabled": "true"
    },
    "properties": {
      "id": {
        "type": "text"
      },
      "source": {
        "type": "text"
      },
	  "question": {
        "type": "text"
      },
	  "page": {
        "type": "text"
      },
	  "category": {
        "type": "text"
      },
	  "generic": {
        "type": "text"
      },
	  "applicant": {
        "type": "text"
      },
	  "issue_date": {
        "type": "date"
      },
	  "r_issue_date": {
        "type": "date"
      },
	  "molecular_weight": {
        "type": "text"
      },
	  "modality": {
        "type": "text"
      },
	  "adaptive_disease": {
        "type": "text"
      },
	  "adm_route": {
        "type": "text"
      },
	  "doc_id": {
        "type": "text"
      },
      "question_vector": {
        "type": "dense_vector",
        "dims": 768
      }
    }
  }
}
```
### 8. Edit bertserving container 


```bash
$ docker exec -it bertsearch_bertserving bash
$ nano /usr/local/lib/python3.5/dist-packages/bert_serving/server/bert/tokenization.py
# tokenization.pyの160行をコメントにする
$ exit 
$ docker restart bertsearch_bertserving
```


### 9. Create documents

Once you created an index, you’re ready to index some document.

```bash
$ python create_documents.py --data=FOLDER_DATA_JSON --index_name=INDEX_NAME
# FOLDER_DATA_JSON
```

After finishing the script, you can get a JSON document like follows:

```python
# documents.jsonl
```

### 10. Index documents

After converting data into a JSON, adds a JSON document to the specified index and makes it searchable.

```bash
$ python example/index_documents.py
```

### 11. Open browser

Go to <http://127.0.0.1:5000>.