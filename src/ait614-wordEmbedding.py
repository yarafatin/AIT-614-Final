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
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from pyspark.sql import SparkSession
import csv

from src import team3ProjectConstants
from src.word_embedding_models import word_embedding_model_logistic


def stratified_split(data_df):
    zeros = data_df.filter(data_df["target"] == 0)
    ones = data_df.filter(data_df["target"] == 1)

    print("original : zeroes count & one count : ", zeros.count(), ones.count(), ones.count() / zeros.count())
    # split datasets into training and testing
    train0, test0 = zeros.randomSplit([0.8, 0.2], seed=1234)
    train1, test1 = ones.randomSplit([0.8, 0.2], seed=1234)

    # stack datasets back together
    train = train0.union(train1)
    test = test0.union(test1)

    print("train : zeroes count & one count : ", train0.count(), train1.count(), train1.count() / train0.count(),
          len(train.collect()))
    print("test : zeroes count & one count : ", test0.count(), test1.count(), test1.count() / test0.count(),
          len(test.collect()))

    stratifiedTrainData = train.sample(False, 10000 / len(train.collect()))

    # x = train.limit(10000)

    #print(" row count:", type(x), train.count(), x.count())

    x_zeros = stratifiedTrainData.filter(stratifiedTrainData["target"] == 0)
    x_ones = stratifiedTrainData.filter(stratifiedTrainData["target"] == 1)

    print("train_10000 : zeroes count & one count : ", x_zeros.count(), x_ones.count(),
          x_ones.count() / x_zeros.count())
    return stratifiedTrainData, train, test

def load_data():
    #csvpath = "../data/train.csv"
    spark = SparkSession.builder.master("local[1]").appName("AIT-614-Project-Team3").getOrCreate()
    data_df = spark.read.format("csv").option("header", "true").load(team3ProjectConstants.trainDataFile, inferSchema="true")

    train10000, train, test =stratified_split(data_df)

    #Just display for time being , delete in final version
    train10000.select("question_text", "target") \
        .where("target == '0'") \
        .show(5)

    train10000.select("question_text", "target") \
        .where("target == '1'") \
        .show(5)
    return train10000, train, test

def load_data_old():
    csvpath = "../data/train.csv"
    spark = SparkSession.builder.master("local[1]").appName("AIT-614-Project-Team3").getOrCreate()
    data_df = spark.read.format("csv").option("header", "true").load(csvpath, inferSchema="true")


    #train, test = train_test_split(data_df, test_size=0.2, stratify=data_df['target'])

    zeros = data_df.filter(data_df["target"] == 0)
    ones = data_df.filter(data_df["target"] == 1)

    print("original : zeroes count & one count : ", zeros.count(), ones.count(), ones.count()/zeros.count())
    # split datasets into training and testing
    train0, test0 = zeros.randomSplit([0.8, 0.2], seed=1234)
    train1, test1 = ones.randomSplit([0.8, 0.2], seed=1234)

    # stack datasets back together
    train = train0.union(train1)
    test = test0.union(test1)

    print("train : zeroes count & one count : ", train0.count(), train1.count(), train1.count()/train0.count(), len(train.collect()))

    x = train.sample(False, 10000 / len(train.collect()))

    #x = train.limit(10000)

    print (" row count:" , type(x), train.count(), x.count())

    x_zeros = x.filter(x["target"] == 0)
    x_ones = x.filter(x["target"] == 1)

    print("train_10000 : zeroes count & one count : ", x_zeros.count(), x_ones.count(), x_ones.count() / x_zeros.count())

    print('#################print sample insincere values ####################')

    x, train, test =stratified_split(data_df)
    x.select("question_text", "target") \
        .where("target == '0'") \
        .show(5)

    x.select("question_text", "target") \
        .where("target == '1'") \
        .show(5)


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

    #TODO - explore
    #MulticlassClassificationEvaluator

def process():
    train10000, train, test = load_data()
    train_x = train10000.select("question_text")
    train_y = train10000.select("target")
    test_x = test.select("question_text")
    test_y = test.select("target")

    predicted = word_embedding_model_logistic(train_x, train_y, test_x)
    print ('prediction done')
    print_performance_report(test_y, predicted, 'Logistic regression model With Glove embeddings')

if __name__ == '__main__':
    print('111')
    process()

