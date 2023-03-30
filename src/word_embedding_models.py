"""
AIT - 614 Final Project - Troll question detection
@author
    Yasser Parambathkandy
    Indranil pal
    Deepak Rajan

Logistic regression and GRU modeling with glove embedding
"""

import pickle

import numpy as np
from sklearn.linear_model import LogisticRegression
from tqdm import tqdm

from text_utils import load_word_tokenizer, stop_words

embedding_file = '../data/glove.840B.300d/glove.840B.300d.txt'
max_length = 300  # max length of words in each question, used for padding to get uniform array length
embed_size = 300  # size of the glove embedding dimension 300, used as input to RNN


def word_embedding_model_logistic(train_x, train_y, test_x):
    """
    logistic regression with glove embedding as the input
    :param train_x:
    :param train_y:
    :param test_x:
    :return:
    """
    print('start logistic regression model with glove embedding')
    # step 1: get embedding dictionary from glove
    embedding_dict = word_embedding_dict()
    # step 2: convert to numpy after some cleanup like stop word removal
    train_embed = np.array([sentence_to_word_embedding(x, embedding_dict) for x in tqdm(train_x)])
    test_embed = np.array([sentence_to_word_embedding(x, embedding_dict) for x in tqdm(test_x)])
    # step 3: train model
    model = LogisticRegression(solver='sag')
    print('start training logistics regression model')
    model.fit(train_embed, train_y)

    # save the model to disk
    pickle.dump(model, open('word_embedding_model_logistic.pkl', 'wb'))
    # step 4: prediction
    return model.predict(test_embed)


def word_embedding_dict():
    """
    read glove embedding from local file. see readme for download instructions
    :return:
    """
    print('read glove word embedding into dict')
    embedding_vector = {}
    with open(embedding_file) as f:
        for line in f:
            line = line.split(' ')
            embedding_vector[line[0]] = np.array(line[1:], dtype=np.float32)
    return embedding_vector


def sentence_to_word_embedding(s, embeddings):
    """
    Perform text cleanup and lookup embedding for works in glove
    :param s:
    :param embeddings:
    :return:
    """
    words = load_word_tokenizer(str(s).lower())
    words = [w for w in words if not w in stop_words]
    words = [w for w in words if w.isalpha()]
    embedding_val = []
    for w in words:
        try:
            embedding_val.append(embeddings[w])
        except:
            continue
    embedding_val = np.array(embedding_val)
    v = embedding_val.sum(axis=0)
    if type(v) != np.ndarray:
        return np.zeros(embed_size)
    return v / np.sqrt((v ** 2).sum())
