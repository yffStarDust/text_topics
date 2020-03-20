#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : szu-hwj

from baseline_gensim import BaselineGensim
from Wmd_model import Wmd_model
from Filter_sentence import load_target_sentence, get_same_rate, length_difference_rate, compute_inverse
import os
import json

"""
与前端的交互接口
输入：input_sentence:用户问题
      model_name:使用哪个模型
      n:需要返回的句子数
输出：
      results_string: json格式的输出，形如：
      {'result1': {'title':用户输入问题, 'split_title': 切分后的输入问题}，
      'result2': {0:{'index':编号, 'similarity': 相似度, 'title': 问题, 'confidence': 可信度}, 1:{},...,n:{}}}
"""

def interface(input_sentence, model_name, n=5):
    cwd = os.getcwd()
    # 应该用异常去判断，否则如果不存在模型，无法得到results参数
    if model_name == 'tfidf':
        with open(cwd + r'\train_questions.json', 'r') as f:
            data = json.load(f)
        model = BaselineGensim()
        results = model.get_topn_sims(input_sentence, n)
    elif model_name == 'wmd':
        with open(cwd + r'\train_questions.json', 'r') as f:
            data = json.load(f)
        model = Wmd_model(data)
        results = model.GetSimilarity(input_sentence, n)
    else:
        print('不存在这个模型')
    target_sentence, target_key = load_target_sentence(results, n)
    confidence = True    # 置信度
    if target_sentence == 0:
        results_string = json.dumps(results)
        return results_string
    else:
        len_diff_rate = length_difference_rate(input_sentence, target_sentence)
        same_rate = get_same_rate(input_sentence, target_sentence, model.stop_list)
        inverse_rate = compute_inverse(input_sentence, target_sentence, model.stop_list)
        incofidence_num = 0  # 以上几种特征工程有多少个认为目标句子不可信
        if len_diff_rate > 2:   # 两个问题长度差100%，这个可以调整
            incofidence_num += 1
        if same_rate < 0.5:
            incofidence_num += 1
        if inverse_rate > 0.5:
            incofidence_num += 1
        # 如果有2个以上认为目标句子不可信就认为该句子不可信
        if incofidence_num >= 2:
            confidence = False
    # 找到对应的要筛选的句子,形如{'index':编号,'similarity':相似度，'title':问题}
        target_result_2 = results['result2'][target_key]
        if not confidence:
            target_result_2['confidence'] = '不准确'
        else:
            target_result_2['confidence'] = '准确'
        results_string = json.dumps(results)
        return results_string


if __name__ == '__main__':
    test_sentence = '“三证合一、一照一码”登记制度改革是什么？具体推行时间和范围是如何规定的'
    sent = '“三证合一、一照一码”登记制度'
    sentences = '财政部国家税务总局关于全面推开营业税改征增值税试点的通知'
    model_name = 'tfidf'
    n = 5
    results= interface(sentences, model_name, n)
    print(results)