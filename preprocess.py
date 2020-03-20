import os
import datetime
import re
import calendar

import pandas as pd
import jieba
import warnings
from bs4 import BeautifulSoup
warnings.filterwarnings('ignore')

from htds.dataset.service.sdk import *


def text_extraction(from_year=2019,
                    from_month=7,
                    from_day=1,
                    to_year=2020,
                    to_month=1,
                    to_day=1):
    """
    Extract the text during the specified time period.
    Clean the data and dump it to csv file.
    :param from_year: int, begin year
    :param from_month: int, begin month
    :param from_day: int, begin day
    :param to_year: int, end year
    :param to_month: int, end month
    :param to_day: int, end day
    :return: pd.DataFrame, the cleaned text
    """
    if not (isinstance(from_year, int) and isinstance(to_year, int)
                and isinstance(from_month, int) and isinstance(to_month, int)):
        raise ValueError("Not all params are int!")
    if from_year > to_year:
        raise ValueError("from_year should be less than to_year!")
    if not (1 <= from_month <= 12 and 1 <= to_month <= 12):
        raise ValueError("Month should be in range [1, 12]!")

    # Generate the start date and end date
    cur_date = datetime.date(from_year, from_month, from_day)
    end_date = datetime.date(to_year, to_month, to_day)

    ds_name = "dw-bigdata-hive"
    htdsc = HTDSContext()
    sql_execute = htdsc.get_public_datasource(ds_name)
    text_df = pd.DataFrame()
    while cur_date <= end_date:
        curdate = cur_date.strftime('%Y%m%d')
        text_df_day = sql_execute.query("""SELECT id, abstract FROM
                                        (
                                            SELECT
                                                id,
                                                abstract,
                                                regexp_replace(substr(pubdate, 1, 10), '-', '') AS pub_date
                                            FROM
                                                src_center_admin.text_basicinfo
                                            WHERE
                                                hdfs_par = {0}
                                                AND hd_business_date = {1}
                                        ) t
                                        WHERE t.pub_date = {2}""".format(curdate[:6], curdate, curdate))
        text_df_day.columns = ['id', 'content']
        text_df = pd.concat([text_df, text_df_day], axis=0, ignore_index=True)
        cur_date = cur_date + datetime.timedelta(days=1)
    chn_ex = re.compile(r'[\u4e00-\u9fa5|\u3002\uff1b\uff0c\uff1a\u201c\u201d\uff08\uff09\u3001\uff1f\u300a\u300b]+')
    text_df.loc[:, 'content'] = text_df['content'].apply(lambda x: text_chn_re(x, chn_ex))
    return text_df
    # The results should be stored in Hive.
    # text_df.to_csv("./data/train/text_content.csv")


def text_extract_html(html, label='p'):
    """
    Extract the text from the specified labels of the given html string
    :param html: Original html string
    :param label: Specified label in the html string
    :return: The concatenated Chinese text extracted from the specified labels of the html string
    """
    soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
    lines = soup.find_all(label)
    label_texts = []
    for line in lines:
        line = line.text.strip().replace('\n', '')
        label_texts.append(line)
    return ' '.join(label_texts)


def text_chn_re(html_str, re_obj):
    """
     Extract Chinese characters only from the given string with regexp
    :param html_str: str, input string which is like "<P class = param>今日" and so on.
    :param re_obj: The compiled regexp object.
    :return: The concatenated Chinese text extracted from the string
    """
    res = re_obj.findall(html_str)
    return ''.join(res)


def pre_process(docdir):
    """
    Perform work-cut and world filtering operation and for all the files under the specified directory
    :param filelocation: type list.The directory where all files stored.
    :return: List of processed docs
    """
    # files = []
    # for root, dirs, docs in os.walk(docdir):
    #     for doc in docs:
    #         if os.path.isfile(os.path.join(root,doc)):
    #             files.append(os.path.abspath(os.path.join(root, doc)))
    file_names = os.listdir(docdir)
    files = [os.path.abspath(os.path.join(docdir, file_name)) for file_name in file_names]
    files = [open(file, encoding='utf-8').read() for file in files]
    docs = [jieba.lcut(file) for file in files]
    filtered_docs = [[word for word in doc if len(word) > 1] for doc in docs]
    corpus = [' '.join(doc) for doc in filtered_docs]
    print('After preprocessing: ', corpus)
    return corpus