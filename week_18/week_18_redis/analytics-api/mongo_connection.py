from dotenv import dotenv_values
from pymongo import MongoClient

config = dotenv_values(".env")

MONGO_URI = config.get("MONGO_URI", "mongodb://127.0.0.1:27017/")
MONGO_DB = config.get("MONGO_DB", "border_alerts_db")


class Mongo:
    def __init__(self, uri, db_name):
        self.client = MongoClient(uri, serverSelectionTimeoutMS=3000)
        self.db = self.client[db_name]

    def collection(self, name):
        return self.db[name]

    def close(self):
        self.client.close()


mongo = Mongo(MONGO_URI, MONGO_DB)