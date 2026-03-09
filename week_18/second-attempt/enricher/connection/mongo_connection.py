import os
from dotenv import dotenv_values
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection

# --- Config ---
ENV = {**dotenv_values(".env.local"), **os.environ}
MONGO_URI = ENV.get("MONGO_URI", "mongodb://127.0.0.1:27017/")
MONGO_DB = ENV.get("MONGO_DB", "pizza_mongo")


class Mongo:
    def __init__(self, uri: str, db_name: str):
        self.client = MongoClient(uri, serverSelectionTimeoutMS=3000)
        self.db: Database = self.client[db_name]

    def collection(self, name: str) -> Collection:
        return self.db[name]

    def close(self):
        self.client.close()


# --- Usage ---
mongo = Mongo(MONGO_URI, MONGO_DB)
