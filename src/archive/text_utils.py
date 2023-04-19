"""
AIT - 614 Final Project - Troll question detection
@author
    Yasser Parambathkandy
    Indranil pal
    Deepak Rajan

Utility class to perform bootstrap and other common activities
"""

import nltk
import numpy as np
from nltk import word_tokenize
from nltk.corpus import stopwords
from sklearn.metrics import f1_score


def load_stop_words():
    try:
        return stopwords.words('english')
    except:
        nltk.download('stopwords')
        return stopwords.words('english')


def load_word_tokenizer(x):
    try:
        return word_tokenize(str(x).lower())
    except:
        nltk.download('punkt')
        return word_tokenize(str(x).lower())


def best_threshold_predicted(test_y, predict):
    best_thresh = 0.0
    best_f1_score = 0.0
    for thresh in np.arange(0.1, 0.501, 0.01):
        thresh = np.round(thresh, 2)
        temp = f1_score(test_y, (predict > thresh).astype(int))
        if temp > best_f1_score:
            best_f1_score = temp
            best_thresh = thresh
    print('with threshold {}, f1 score is {}'.format(best_thresh, best_f1_score))
    return (predict > best_thresh).astype(int)


stop_words = load_stop_words()
