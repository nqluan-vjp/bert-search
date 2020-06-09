#!/bin/sh
bert-serving-start -cased_tokenization -num_worker=1 -model_dir /model
