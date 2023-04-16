import os

MONGO_DB_USER = "yparamba"
MONGO_DB_NAME = "ait614"
MONGO_DB_COLLECTION = "quoraQuestions"

if os.environ.get("FLASK_ENV") == 'cloud':
    MONGO_DB_HOST = "ait614.adkj20o.mongodb.net"
    MONGO_DB_PASSWORD = "OUGAsNCiJKp0oDUU"
    TRAIN_FILE_PATH = "../data/train.csv"
    WORD_EMBEDDING_MODEL_SAVE_PATH = "sincerity.model"
    IS_CLOUD = True
else:
    MONGO_DB_HOST = "localhost"
    MONGO_DB_PASSWORD = "OUGAsNCiJKp0oDUU"
    TRAIN_FILE_PATH = "../data/train.csv"
    WORD_EMBEDDING_MODEL_SAVE_PATH = "sincerity.model"
    IS_CLOUD = False
