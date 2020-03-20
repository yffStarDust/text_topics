#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : szu-hwj

import gensim
import pandas as pd
import jieba
import os
import json
import Data



class BaselineGensim(object):
    def __init__(self):
        self.cwd = os.getcwd()
        with open(self.cwd + r'\train_questions.json', 'r') as f:
            data = json.load(f)
            self.titles = []  # 未分词的问题
            self.content = [] # 已分词去停用词的问题
            for i in range(len(data)):
                self.titles.append(data[i]["title"])
                self.content.append(data[i]["split_title"])
        self.content_list = [line.rstrip().split() for line in self.content]
        with open(self.cwd+'\stop_words.txt', encoding='utf-8') as f:
            lines = f.readlines()
        self.stop_list = [x.strip() for x in lines]
        self.dictionary = self.bulid_dictionary()
        corpus = [self.dictionary.doc2bow(line) for line in self.content_list]
        num_features = max(self.dictionary.token2id.values())
        self.tfidf = gensim.models.TfidfModel(corpus)
        self.idx = gensim.similarities.MatrixSimilarity(self.tfidf[corpus])

    @staticmethod
    def split_word(query, stop_list):
        words = jieba.cut(query)
        result = ' '.join([word for word in words if word not in stop_list])
        return result

    def bulid_dictionary(self):
        """
        得到一个基于数据集的字典，每个词的编号
        :return:
        """
        if os.path.exists(self.cwd+r'\question_dictionary.dict'):
            dictionary = gensim.corpora.Dictionary.load(self.cwd+r'\question_dictionary.dict')
        else:
            content_list = [line.rstrip().split() for line in self.content]
            dictionary = gensim.corpora.Dictionary(content_list)
            dictionary.save(self.cwd+r'\question_dictionary.dict')
        return dictionary

    # def build_model(self):
    #     corpus = [self.dictionary.doc2bow(line) for line in self.content_list]
    #     num_features = max(self.dictionary.token2id.values())
    #     tfidf = gensim.models.TfidfModel(corpus)
    #     # if self.model_name == 'lsi':
    #     #     model = gensim.models.LsiModel(corpus)
    #     #     idx = gensim.similarities.SparseMatrixSimilarity(model[corpus], num_features=num_features)
    #     # else:
    #     idx = gensim.similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=num_features)
    #     # idx = gensim.similarities.SparseMatrixSimilarity(tfidf[corpus])
    #     return idx, tfidf

    def get_topn_sims(self, sentences, n=5):
        """
        输入问题找出对应的前n相似度的编号
        :param sentences: 输入问题
        :param n: 默认输出5条
        :return:
        """
        split_sent = self.split_word(sentences, self.stop_list).split()
        # 得到匹配结果1
        results_1 = {'title':sentences, 'split_title': split_sent}
        vec = self.dictionary.doc2bow(split_sent)
        sims = self.idx[self.tfidf[vec]]
        similarities = list(enumerate(sims))
        dict_sims = dict(similarities)
        sorted_sims = sorted(dict_sims.values(), reverse=True)

        # 去除匹配到与原问题一样的结果，认为原问题的相似度一定最高，否则模型有问题
        top_sim_num = list(dict_sims.values()).index(sorted_sims[0])
        first = 0
        self.titles[top_sim_num] = ''.join(self.titles[top_sim_num].split())
        if sentences == self.titles[top_sim_num]:
            # 如果相似度最高的句子是原问题，则从下一条匹配问题开始读取
            first += 1
        topn_sims = sorted_sims[first:n+first]

        topn_queries_num = [list(dict_sims.values()).index(i) for i in topn_sims]  # 选出的n个问题的编号
        topn_queries = [self.titles[i] for i in topn_queries_num] # 选出的n个问题
        topn_values = [dict_sims[i] for i in topn_queries_num]  # 选出的n个问题的相似度
        # 得到匹配结果2
        # results_2 = {}
        results_2 = []
        for i in range(n):
            each = [topn_queries_num[i], topn_queries[i], topn_values[i]]
            each_results_2 = {'index':str(topn_queries_num[i]), 'similarity':str(topn_values[i]), 'title':topn_queries[i],
                              'confidence':None}
            results_2.append(each_results_2)
        # 汇总结果1和结果2
        results = {'result1': results_1, 'result2': results_2}
        return results


if __name__ == '__main__':
    # dir_path = r'E:\2018上\自学方向\磐创\项目\会学项目'
    baseline = BaselineGensim()
    test_sentence = '国家税务总局关于调整中国国电集团公司合并纳税范围的通知'
    results = baseline.get_topn_sims(test_sentence)
    print(results)
