#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : szu-hwj

import json
import pandas as pd
import os
import jieba
import time

class Data:
    """
    对数据集进行处理，得到以外格式的数据：
    csv文件：原问题和分词去停用词的问题
    json文件：将问题保存成json文件，为一个list，list中每个元素为一个字典{title:原问题, split_title:切分去停用问题}
    对于每个数据集，只需要输入数据集名和停用词，就都能得到以上两个文件，方便复用
    """
    def __init__(self, filename, stoplist_name):
        self.cwd = os.getcwd()
        self.filename = filename
        self.stop_list = self.get_stoplist(stoplist_name)

    def excel2csv(self):
        """
        用户导入的数据在../myuploads,'qa.xlsx'或者'qa.xls'两种格式
        将用户导入的数据转成csv并保存在当前路径下
        :return:
        """
        paths = self.cwd.split('\\')
        last_path_len = len(paths[-1])
        # 用户上传数据存放的文件夹
        path = self.cwd[:-last_path_len] + 'myuploads'
        # 用户上传数据的文件名，默认文件夹中只有一个用户上传的文件
        data_path = os.listdir(path)[0]
        if data_path.endswith('xlsx') or data_path.endswith('xls'):
            dataset = pd.read_excel(path + '\\' + data_path)
            dataset.to_csv(self.cwd + '\\qa.csv', index=False)
        else:
            # 当用户上传的不是excel文件的时候，对用户进行提示，后面在补充
            pass

    @staticmethod
    def get_stoplist(stoplist_name):
        """
        读取停用词
        :param stoplist_name: 停用词的路径
        :return:
        """
        with open(stoplist_name, encoding='utf-8') as f:
            stop_word = f.readlines()
        stop_list = [x.strip() for x in stop_word]
        return stop_list

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

    def split_dataset(self):
        """
        对数据集所有问题进行切词，title列表示未切割问题，split_title表示已经切割
        :return:
        """
        file_path = self.cwd + '\\' + self.filename
        f = open(file_path, encoding='gbk')
        df_dataset = pd.read_csv(f)
        f.close()
        collumns_name = list(df_dataset.columns)[0]
        df_dataset.rename(columns={collumns_name: 'title'}, inplace=True)
        df_dataset['split_title'] = df_dataset['title'].apply(lambda x: self.split_word(x))
        save_filename = 'df_' + self.filename
        df_save_path = self.cwd + '\\' + save_filename # DataFrame格式的数据存放路径
        df_dataset.to_csv(df_save_path, index=False)
        return df_dataset

    def get_dataset(self):
        """
        读取json格式的数据
        :return:
        """
        # 如果路径中存在了json数据就直接读取，若没有就对原数据进行处理
        json_path = self.cwd + '\\' +self.filename[:-4] + '.json'
        save_filename = 'df_' + self.filename
        df_save_path = self.cwd + '\\' + save_filename # DataFrame格式的数据存放路径
        if os.path.exists(json_path):
            with open(json_path) as f:
                data = json.load(f)
        else:
            if os.path.exists(df_save_path):
                f = open(df_save_path, encoding='gbk')
                df_dataset = pd.read_csv(f)
                f.close()
            else:
                df_dataset = self.split_dataset()
            data = []  # 转变df_dataset的格式与伦青的一致
            for i in range(len(df_dataset)):
                dict_sample = dict(df_dataset.iloc[i])
                data.append(dict_sample)
            with open(json_path, 'w') as f:
                json.dump(data, f)
        # return data


def merge_json(insert_filename, total_filename='total_dataset.json'):
    """
    该函数用来将新增的数据加到总的json文件中
    :param insert_filename: 需要加入的数据的json文件
    :param total_filename: 总的数据的json文件
    :return:
    """
    cwd = os.getcwd()
    total_path = cwd + '\\' + total_filename
    insert_path = cwd + '\\' + insert_filename
    with open(insert_path) as f:
        insert_data = json.load(f)
    if not os.path.exists(total_path):
        with open(total_path, 'w') as f:
            json.dump(insert_data, f)
    else:
        with open(total_path) as f:
            total_data = json.load(f)
        total_data.extend(insert_data)
        with open(total_path, 'w') as f:
            json.dump(total_data, f)



if __name__ == '__main__':
    start = time.time()
    cwd = os.getcwd()
    # file_name = 'train_questions.csv'
    file_name = 'qa.csv'
    stoplist_name = 'stop_words.txt'
    data = Data(file_name, stoplist_name)
    data.excel2csv()
    data.get_dataset()
    # data = data.get_dataset()
    print('spent %.2f times to load data' % (time.time()-start))
    # print(data[0])

