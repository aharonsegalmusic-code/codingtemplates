import json
from os import getenv
from pymongo import MongoClient

mongo_uri = getenv("MONGO_URI", "mongodb://localhost:27017/")
mongo_db = getenv("MONGO_DB", "testdb")
mongo_collection = getenv("MONGO_COLLECTION", "testcollection")
file_path = getenv("JSON_FILE_PATH", "./employee_data_advanced.json")

client = MongoClient(mongo_uri)
db = client[mongo_db]
collection = db[mongo_collection]

with open(file_path, "r", encoding="utf-8") as file:
    file_data = json.load(file)

result = collection.insert_many(file_data)
print("data inserted to mongodb")
print("documents inserted:", len(result.inserted_ids))

client.close()