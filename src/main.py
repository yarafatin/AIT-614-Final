"""
AIT - 614 Final Project - Troll question detection
@author
    Yasser Parambathkandy
    Indranil pal
    Deepak Rajan

Main processing is done in this file.
Two models are created and compared for performance
1) Logistic Regression with glove embeddings
2) Logistic Regression with sentence embeddings

"""

import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

from sentence_embedding_models import sentence_embedding_model_logistic
from word_embedding_models import word_embedding_model_logistic

input_data_path = '../data/train.csv'


def process():
    """
    The process function load data from file system, creates and compares models to detected insincere questions
    Glove and Universal sentence embeddings have been used to compare performance
    Logistic regression has been used as a supervised learning model
    """

    print('starting word embedding based modeling')
    data_df = load_data()
    print('\ndata loaded')
    # class is highly imbalanced - only 6% insincere question, so split train/test data with similar proportion
    # "stratify" is used to maintain class ratio on both data sets
    train, test = train_test_split(data_df, test_size=0.2, stratify=data_df['target'])
    train_insincere_q = train[train['target'] == 1]
    test_insincere_q = test[test['target'] == 1]
    # verify percentage of insincere qs after split is 6% on both data sets
    print('training dataset insincere questions - {}%'.format(len(train_insincere_q) * 100 / len(train)))
    print('test dataset insincere questions - {}%'.format(len(test_insincere_q) * 100 / len(test)))

    train_x, train_y, test_x, test_y = train['question_text'].values, train['target'].values, \
                                       test['question_text'].values, test['target'].values

    # model 1 - Logistic Regression with glove embedding
    predicted = word_embedding_model_logistic(train_x, train_y, test_x)
    print_performance_report(test_y, predicted, 'Logistic regression model With Glove embeddings')

    # model 2 - Logistic Regression with sentence embedding
    predicted = sentence_embedding_model_logistic(train_x, train_y, test_x)
    print_performance_report(test_y, predicted, 'Logistic regression model with sentence embeddings')


def print_performance_report(test_y, predicted, model_desc):
    """
    print performance report of model - accuracy, precision, recall, f1 score, confusion matrix
    :param test_y:
    :param predicted:
    :param model_desc:
    :return:
    """
    print('printing performance report of {}'.format(model_desc))
    print("Accuracy : {}".format(accuracy_score(test_y, predicted)))
    print("The Classification Report : ")
    print(classification_report(test_y, predicted))
    print("Confusion Matrix : ")
    print(confusion_matrix(test_y, predicted))


def load_data():
    """
    load data from file system and print samples
    :return:
    """
    all_data_df = pd.read_csv(input_data_path)
    print('#################print sample insincere values ####################')
    print(all_data_df[all_data_df['target'] == 1]['question_text'].sample(5))
    print('#################print sample sincere values ####################')
    print(all_data_df[all_data_df['target'] == 0]['question_text'].sample(5))
    return all_data_df

    # For local development, limit data to 10K for easier development and testing
    # make sure in that 10k, there are some insincere questions.
    # uncomment below that does it
    # a = all_data_df[all_data_df['target'] == 1].sample(600)
    # b = all_data_df.sample(10000)
    # return pd.concat([a, b])


if __name__ == '__main__':
    process()
