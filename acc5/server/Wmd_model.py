#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : szu-hwj

import csv
from time import time
import pickle
from gensim.models import Word2Vec
import jieba
from gensim.similarities import WmdSimilarity

import os
# from Data import split_word
import json

class Wmd_model:
    def __init__(self, data, w2v_size=64):
        self.cwd = os.getcwd()
        with open(self.cwd+'\stop_words.txt', encoding='utf-8') as f:
            lines = f.readlines()
        self.stop_list = [x.strip() for x in lines]

        self.data = data  # json格式的数据集
        self.titles = []  # 未分词的问题
        self.content = [] # 已分词去停用词的问题
        for i in range(len(data)):
            self.titles.append(data[i]["title"])
            self.content.append(data[i]["split_title"])

        # 使用content数据训练词向量 w2v_size为词向量大小
        w2v_start = time()
        self.w2v_model = Word2Vec(self.content, workers=3, size=w2v_size)
        w2v_end = time()
        print('w2v took %.2f seconds to run.' % (w2v_end - w2v_start))


    def split_word(self, query):
        """
        结巴分词，去除停用词
        :param query: 待切问题
        :param stop_list: 停用词表
        :return:
        """
        words = jieba.cut(query)
        result = ' '.join([word for word in words if word not in self.stop_list])
        return result

    def GetSimilarity(self, sentences, num_best=5):
        """
        :param sentences: 用户输入的问题
        :param num_best: 要获得的相似问题的个数
        :return:
        """
        self.num_best = num_best
        start = time()

        # 初始化生成WmdSimilarity对象,匹配多一条，如果匹配到原问题就去掉
        instance = WmdSimilarity(self.content, self.w2v_model, num_best=num_best+1)
        # 对输入的句子进行分词和去停用词
        split_sent = self.split_word(sentences)
        # 得到匹配结果1
        results_1 = {'title':sentences, 'split_title': split_sent.split()}
        # if self.verbose:
        #     print("result:", result)
        sims = instance[split_sent]  # 形如[(匹配问题编号, 相似度)]
        # 去除匹配到与原问题一样的结果，认为原问题的相似度一定最高，否则模型有问题
        # max_sim_index = -1
        # max_sim = 0
        # for i, sim in enumerate(sims):
        #     if sim[2] > max_sim:
        #         max_sim_index = i
        #         max_sim = sim[1]

        # 相似度最高的放在sims的第0个
        top_sim_num = sims[0][0]  # 相似度最高问题的编号
        self.titles[top_sim_num] = ''.join(self.titles[top_sim_num].split())
        if sentences == self.titles[top_sim_num]:
            sims.remove(sims[0])
        else:
            sims = sims[:-1]
        results_2 = []
        # 得到匹配结果2
        for i, sim in enumerate(sims):
            question_num = sim[0] # 匹配问题的编号
            question = self.titles[question_num]
            each_results_2 = {'index':str(question_num), 'similarity':str(sim[1]), 'title':question, 'confidence':None}
            results_2.append(each_results_2)
        # 汇总结果1和结果2
        results = {'result1': results_1, 'result2': results_2}
        # if self.verbose:
        print('Cell took %.2f seconds to run.' % (time() - start))
        return results


if __name__ == '__main__':
    cwd = os.getcwd()
    # with open(cwd + r'\total_dataset.json', 'r') as f:
    with open(cwd + r'\train_questions.json', 'r') as f:
        data = json.load(f)
    wmd_model = Wmd_model(data)
    sent = '“三证合一、一照一码”登记制度改革是什么？具体推行时间和范围是如何规定的'
    results = wmd_model.GetSimilarity(sent)
    print('finished!')
    print(results)