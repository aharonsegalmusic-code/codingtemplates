import os
from pymongo import MongoClient

class MongoDB:
    def __init__(self):
        mongodb_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
        db_name = os.getenv("MONGODB_DB", "practice")

        self.client = MongoClient(mongodb_uri, serverSelectionTimeoutMS=3000)
        self.db = self.client[db_name]
        self.db_name = db_name

    def ping(self) -> None:
        self.client.admin.command("ping")

    def close(self) -> None:
        self.client.close()