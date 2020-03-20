#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : szu-hwj

from Data import Data


def upload_interface():
    """
    上传事件接口：当用户点击上传之后触发该事件，将用户上传的excel数据转换成json格式
    :return:
    """
    file_name = 'qa.csv'
    stoplist_name = 'stop_words.txt'
    data = Data(file_name, stoplist_name)
    data.excel2csv()
    data.get_dataset()


if __name__ == '__main__':
    upload_interface()