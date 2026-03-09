from dotenv import dotenv_values
from pymongo import MongoClient

class Mongo:
    def __init__(self, uri, db_name):
        self.client = MongoClient(uri, serverSelectionTimeoutMS=3000)
        self.db = self.client[db_name]

    def collection(self, name):
        return self.db[name]

    def close(self):
        self.client.close()


# mongo = Mongo(MONGO_URI, MONGO_DB)