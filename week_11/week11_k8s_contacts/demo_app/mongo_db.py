import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

class MongoInstance:
    _instance = None
    @staticmethod
    def instance():
        if MongoInstance._instance is None:
            # Use authSource=admin for root credentials
            user = os.getenv('MONGO_INITDB_ROOT_USERNAME')
            password = os.getenv('MONGO_INITDB_ROOT_PASSWORD')
            host = os.getenv('MONGO_NAME', 'mongo-db')
            port = os.getenv('DATABASE_PORT', '27017')
            db_name = os.getenv('MONGO_INITDB_ROOT_DATABASE')
            
            mongo_url = f"mongodb://{user}:{password}@{host}:{port}/{db_name}?authSource=admin"
            MongoInstance._instance = MongoClient(mongo_url)
        return MongoInstance._instance

mongo_client = MongoInstance.instance()
