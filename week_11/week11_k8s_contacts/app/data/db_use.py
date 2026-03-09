"""
This file handles the MongoDB connection:
    Create MongoDB connection (using environment variables for host/port)
    Basic connection test
"""
from pymongo import MongoClient
import os
from dotenv import load_dotenv
# from pathlib import Path

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

def basic_crud_test():
    """
    Test MongoDB by:
    1. pinging the server
    2. inserting a test document
    3. reading that document back
    4. deleting it
    returns a dict with status messages and data
    """
    # start client
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]

    message_dict = {}

    try:
        # 1. ping the server
        client.admin.command("ping")
        message_dict["ping"] = "✅ ping successful: connected to MongoDB"

        # 2. inserting a test document
        test_collection = db["test_connection_collection"]
        insert_result = test_collection.insert_one({"test": "mongo_connection", "ok": True})
        message_dict["insert"] = {
            "message": "✅ inserted test document",
            "inserted_id": str(insert_result.inserted_id),
        }

        # 3. reading that document back
        found_doc = test_collection.find_one({"_id": insert_result.inserted_id})
        # Convert ObjectId to string for safer printing/JSON
        if found_doc and "_id" in found_doc:
            found_doc["_id"] = str(found_doc["_id"])
        message_dict["find"] = {
            "message": "✅ found document",
            "document": found_doc,
        }

        # 4. deleting it
        test_collection.delete_one({"_id": insert_result.inserted_id})
        message_dict["delete"] = "✅ deleted test document"

        return message_dict

    except Exception as e:
        print("❌ error while testing MongoDB connection:", e)
        raise

    finally:
        client.close()
        print("MongoDB client closed")



