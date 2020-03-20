import collections
import random
import pandas as pd
import jieba
from gensim.models.word2vec import Word2Vec
import warnings
warnings.filterwarnings('ignore')

from htds.dataset.service.sdk import *

random.seed = 16

"""
# Assume that text has been extracted from DB
ds_name = "dw-bigdata-hive"
htdsc = HTDSContext()
sql_execute = htdsc.get_public_datasource(ds_name)
title_df = sql_execute.query('SELECT id, texttitle FROM text_basicinfo WHERE hdfs_par = "202001" AND '
                             'hd_business_date = "20200107"')
"""
stopwords = []
with open("stopwords.txt") as f:
    for line in f.readlines():
        line = line.strip()
        stopwords.append(line)


def segWord(doc):
    seg_list = jieba.cut(doc, cut_all=False)
    return list(seg_list)


# Remove stop words
def filter_map(arr):
    res = ""
    for c in arr:
        if c not in stopwords and c != ' ' and c != '\xa0' and c != '\n' and c != '\ufeff' and c != '\r':
            res += c
    return res


# move stop words and generate char sent
def filter_char_map(arr):
    res = []
    for c in arr:
        if c not in stopwords and c != ' ' and c != '\xa0' and c != '\n' and c != '\ufeff' and c != '\r':
            res.append(c)
    return " ".join(res)


# get char of sentence
def get_char(arr):
    res = []
    for c in arr:
        res.append(c)
    return list(res)


data.content = data.content.map(lambda x: filter_map(x))
data.content = data.content.map(lambda x: get_char(x))

data["content"].head()
data.to_csv("preprocess/train_char.csv", index=None)
line_sent = []
for s in data["content"]:
    line_sent.append(s)
word2vec_model = Word2Vec(line_sent, size=100, window=10, min_count=1, workers=4, iter=15)
word2vec_model.wv.save_word2vec_format("word2vec/chars.vector", binary=True)
