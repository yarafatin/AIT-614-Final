"""
AIT - 614 Final Project - Troll question detection
@author
    Yasser Parambathkandy
    Indranil pal
    Deepak Rajan

Logistic regression with sentence embedding
"""
import pickle

import tensorflow_hub as hub
from sklearn.linear_model import LogisticRegression

# google's universal sentence encoder from tf hub
universal_sentence_encoder_url = 'https://tfhub.dev/google/universal-sentence-encoder/4'
embed = hub.load(universal_sentence_encoder_url)


def sentence_embedding_model_logistic(train_x, train_y, test_x):
    """
    simple logistics regression with universal sentence encoder
    :param train_x:
    :param train_y:
    :param test_x:
    :return:
    """
    print('start logistic regression model with sentence embedding')
    # step 1 - get sentence embeddings for both training and test
    train_x = embed(train_x).numpy()
    test_x = embed(test_x).numpy()
    # step 2 - create and train model
    model = LogisticRegression(solver='sag')
    print('start training logistics regression model')
    model.fit(train_x, train_y)
    # save the model to disk
    pickle.dump(model, open('sentence_embedding_model_logistic.pkl', 'wb'))
    # step 2 - predict  model
    return model.predict(test_x)
