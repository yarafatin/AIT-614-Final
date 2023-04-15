import csv

from project_properties import mongo_db_host, mongo_db_user, mongo_db_password, mongo_db_name, \
    mongo_db_collection, trainDataFile
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


def import_data():
    uri = f"mongodb+srv://{mongo_db_user}:{mongo_db_password}@{mongo_db_host}/?retryWrites=true&w=majority"
    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))
    client.admin.command('ping')
    print("Connection successfully connected to MongoDB!")
    db = client[mongo_db_name]
    collection = db[mongo_db_collection]
    # create an index on the qid field
    collection.create_index('qid')

    buffer = []
    buffer_size = 5000

    # open the CSV file and read its contents
    with open(trainDataFile, "r") as csvfile:
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
    import_data()
