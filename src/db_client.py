import csv
import json
import uuid

from pymongo import DESCENDING

from project_properties import MONGO_DB_HOST, MONGO_DB_USER, MONGO_DB_PASSWORD, MONGO_DB_NAME, \
    MONGO_DB_COLLECTION, TRAIN_FILE_PATH
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = f"mongodb+srv://{MONGO_DB_USER}:{MONGO_DB_PASSWORD}@{MONGO_DB_HOST}/?retryWrites=true&w=majority"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
client.admin.command('ping')
print("Connection successfully connected to MongoDB!")
db = client[MONGO_DB_NAME]
collection = db[MONGO_DB_COLLECTION]


def save_question(question_text, prediction):
    # generate a UUID for the qid field
    qid = str(uuid.uuid4())
    # create a dictionary with the document data
    document = {
        "qid": qid,
        "question_text": question_text,
        "target": prediction
    }
    # insert the document into the collection
    collection.insert_one(document)

    print('saved document {}'.format(document))


def get_recent_questions():
    print('getting 10 most recent submissions')
    # Get the most recent 10 documents
    cursor = collection.find().sort('_id', DESCENDING).limit(10)

    # Convert documents to a JSON array
    json_docs = []
    for doc in cursor:
        json_doc = {
            'id': str(doc['_id']),
            'question_text': doc['question_text'],
            'target': doc['target']
        }
        json_docs.append(json_doc)
    print('returning 10 most recent submissions')
    return json_docs


def import_onetime_data():
    if collection.count_documents({}) > 0:
        print('data already exists, not importing again')
        return

    # create an index on the qid field
    collection.create_index('qid')

    buffer = []
    buffer_size = 5000

    # open the CSV file and read its contents
    with open(TRAIN_FILE_PATH, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # add the row to the insert buffer
            buffer.append({
                "qid": row["qid"],
                "question_text": row["question_text"],
                "target": row["target"]
            })

            # if the buffer is full, insert the documents into the collection
            if len(buffer) == buffer_size:
                collection.insert_many(buffer, ordered=False)
                print('inserted 5000 records')
                buffer = []

        # insert any remaining documents in the buffer
        if len(buffer) > 0:
            collection.insert_many(buffer, ordered=False)

    print('all loaded')
    # close the MongoDB connection
    client.close()


if __name__ == '__main__':
    import_onetime_data()
