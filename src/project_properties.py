"""
AIT 614 - Big Data Essentials
DL2 Team 3 Final Project
Detecting Abrasive online user content

Team 3
Yasser Parambathkandy
Indranil Pal
Deepak Rajan

University
George Mason University
"""

"""
This file contains all the properties required for the project.
"""

import os

MONGO_DB_USER = "yparamba"
MONGO_DB_NAME = "ait614"
MONGO_DB_COLLECTION = "quoraQuestions"

# properties to use in cloud. update as required
if os.environ.get("FLASK_ENV") == 'cloud':
    # the mongo db should be configured to allow for the ip to access
    MONGO_DB_HOST = "ait614.adkj20o.mongodb.net"
    MONGO_DB_PASSWORD = "OUGAsNCiJKp0oDUU"
    MONGO_URI = f"mongodb+srv://{MONGO_DB_USER}:{MONGO_DB_PASSWORD}@{MONGO_DB_HOST}/?retryWrites=true&w=majority"
    TRAIN_FILE_PATH = "../data/train.csv"
    MODEL_PATH = "20230419230905-sentence-model"
    IS_CLOUD_ENV = True
# properties to use in local. update as required
else:
    MONGO_URI = 'mongodb://localhost:27017/'
    TRAIN_FILE_PATH = "../data/train.csv"
    MODEL_PATH = "20230419230905-sentence-model"
    IS_CLOUD_ENV = False
