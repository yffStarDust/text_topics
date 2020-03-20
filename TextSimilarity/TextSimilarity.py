import pickle

from keras.preprocessing import text, sequence
from gensim.models.keyedvectors import KeyedVectors
import numpy as np
from htds.dataset.service.sdk import *


class TextSimilarity:
    """
    Pretrain the word2vec embeddings for the words in corpus.
    And then obtain the sentence representation with w2v embedding weighted by tfidf.
    Also provide the interface to retrieve the top k similar sentences
    """
    def __init__(self,
                 sql_execute,
                 embedding_size=100,
                 vocab_size=10000):
        self.vocab_size = vocab_size
        self.embedding_size = embedding_size
        self.sql_execute = sql_execute

    def generateW2V(self, ):
        """
        Generate the W2V embedding for the corpus
        :return:
        """
        data = []
        tokenizer = text.Tokenizer(num_words=None)
        tokenizer.fit_on_texts(data["content"].values)
        with open('tokenizer_char.pickle', 'wb') as handle:
            pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

        word_index = tokenizer.word_index
        w2_model = KeyedVectors.load_word2vec_format("word2vec/chars.vector", binary=True, encoding='utf8',
                                                     unicode_errors='ignore')
        embeddings_index = {}
        embeddings_matrix = np.zeros((len(word_index) + 1, w2_model.vector_size))
        word2idx = {"_PAD": 0}
        vocab_list = [(k, w2_model.wv[k]) for k, v in w2_model.wv.vocab.items()]

        for word, i in word_index.items():
            if word in w2_model:
                embedding_vector = w2_model[word]
            else:
                embedding_vector = None
            if embedding_vector is not None:
                embeddings_matrix[i] = embedding_vector


    def load(self, ):
        with open('tokenizer_char.pickle', 'rb') as handle:
            maxlen = 1000
            model_dir = "model_rcnn_char/"
            tokenizer = pickle.load(handle)
            word_index = tokenizer.word_index
            validation = pd.read_csv("preprocess/test_char.csv")
            validation["content"] = validation.apply(lambda x: eval(x[1]), axis=1)
            X_test = validation["content"].values
            list_tokenized_validation = tokenizer.texts_to_sequences(X_test)
            input_validation = sequence.pad_sequences(list_tokenized_validation, maxlen=maxlen)
            w2_model = KeyedVectors.load_word2vec_format("word2vec/chars.vector", binary=True, encoding='utf8',
                                                         unicode_errors='ignore')
            embeddings_index = {}
            embeddings_matrix = np.zeros((len(word_index) + 1, w2_model.vector_size))
            word2idx = {"_PAD": 0}
            vocab_list = [(k, w2_model.wv[k]) for k, v in w2_model.wv.vocab.items()]
            for word, i in word_index.items():
                if word in w2_model:
                    embedding_vector = w2_model[word]
                else:
                    embedding_vector = None
                if embedding_vector is not None:
                    embeddings_matrix[i] = embedding_vector

    def topK(self, text_id, K):
        pass
