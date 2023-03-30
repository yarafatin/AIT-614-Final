from pymongo import MongoClient
import csv
import team3ProjectConstants

global quoraQuestions
global team3ProjectDb


def setup():
    mongoClient = MongoClient(team3ProjectConstants.mongo_db_url)
    global team3ProjectDb
    team3ProjectDb = mongoClient[team3ProjectConstants.project_db_name]
    global quoraQuestions
    quoraQuestions = team3ProjectDb[team3ProjectConstants.question_collection_name]
    print("total records :", team3ProjectDb.quoraQuestions.estimated_document_count())


def process():
    global quoraQuestions
    global team3ProjectDb
    print('Start Import')

    csvfile = open(team3ProjectConstants.importFile, "r", encoding='utf-8')
    reader = csv.DictReader(csvfile)

    header = ["qid", "question_text", "target"]
    i = 0
    for each in reader:
        row = {}

        for field in header:
            row[field] = each[field]

        i = i + 1
        print(" Inserting record :", i)
        quoraQuestions.insert_one(row)

    print(" Done... :")

    print("total records in MongoDB:", team3ProjectDb.quoraQuestions.estimated_document_count())


# if __name__ == '__main__':
#     setup()
#     process()
