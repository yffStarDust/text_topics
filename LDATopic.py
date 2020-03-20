import os
import pickle

import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from bs4 import BeautifulSoup

# from htds.dataset.service.sdk import *
from preprocess import *


def lda_train(corpus,
              max_features=5000,
              n_topics=300):
    """
    Compute the topic distribution of the given docs with LDA model.
    :param corpus: the docs after pre_processing, like ['我 喜欢 苹果'， '美丽 古老的 国度']
    :param tfidf: TfidfVectorizer instance
    :return: The list of the topic distributions of the docs
    """
    tfidf = TfidfVectorizer(max_features)
    tfidf_matrix = tfidf.fit_transform(corpus)
    with open('./data/model/tfidf.pickle', 'wb') as handle:
        pickle.dump(tfidf, handle, protocol=pickle.HIGHEST_PROTOCOL)
    print("tfidf dumped!")
    print('word frequency matrix: ', tfidf_matrix.toarray())
    # n_components
    lda = LatentDirichletAllocation(n_components=n_topics, random_state=123456)
    res = lda.fit_transform(tfidf_matrix)
    print("LDA training finished!")
    with open('./data/model/lda.pickle', 'wb') as handle:
        pickle.dump(lda, handle, protocol=pickle.HIGHEST_PROTOCOL)
    print("LDA model dumped successfully!")
    print("Topic distribution on training dataset", res)
    return res


def lda_train_1(corpus, n_topics=2):
    """
    Compute the topic distribution of the given docs with LDA model.
    :param corpus: the docs after pre_processing, like ['我 喜欢 苹果'， '美丽 古老的 国度']
    :param tfidf: TfidfVectorizer instance
    :return: The list of the topic distributions of the docs
    """
    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(corpus)
    print("tfidf dumped!")
    print('word frequency matrix: ', tfidf_matrix.toarray())
    # n_components
    lda = LatentDirichletAllocation(n_components=n_topics, random_state=123456)
    res = lda.fit_transform(tfidf_matrix)
    print("Topic distribution on training dataset", res)
    return tfidf_matrix, lda


if __name__ == '__main__':
    corpus = pre_process('data')
    res, lda = lda_train_1(corpus)
