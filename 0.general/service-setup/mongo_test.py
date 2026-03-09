# mongo_test.py
#
# Goal
# - connect to MongoDB
# - TEST DB NAME: ensure the database exists (Mongo creates DB only after data is stored)
# - TEST DB COLLECTION: ensure a collection exists
# - run a test query and print results
#
# Reads configuration ONLY from an env file (NOT from OS environment)
#
# install:
#   pip install pymongo python-dotenv
#
# env files:
#   .env.local  (for running this script on your PC)
#   .env.prod   (for production)
#
# required env vars:
#   MONGO_URI
#   MONGO_DB
#   MONGO_COLLECTION
#
# usage:
#   python mongo_test.py

from __future__ import annotations

from datetime import datetime, timezone
from dotenv import dotenv_values

# =========================================================
# ENV FILE MODE (change this)
# =========================================================
PRODUCTION = False  # False -> .env.local, True -> .env.prod

ENV_PATH = ".env.prod" if PRODUCTION else ".env.local"
ENV = dotenv_values(ENV_PATH)  # NOTE: reads ONLY from the file, does NOT use os.environ


def must_get(key: str) -> str:
    v = ENV.get(key)
    if v is None or str(v).strip() == "":
        raise RuntimeError(f"Missing required key in {ENV_PATH}: {key}")
    return str(v)


MONGO_URI = must_get("MONGO_URI")
MONGO_DB = must_get("MONGO_DB")
MONGO_COLLECTION="test_collection"
# script flags
INIT_DB_AND_COLLECTION = True  # creates db/collection by inserting a persistent init doc (recommended)


def main():
    from pymongo import MongoClient

    print("mongo settings:")
    print(f"  uri={MONGO_URI}")
    print(f"  db={MONGO_DB}")
    print(f"  collection={MONGO_COLLECTION}")

    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)

    # basic connectivity test
    client.admin.command("ping")
    print("TEST CONNECT: ping -> OK")

    # Mongo only shows a DB after it has data
    existing_dbs = client.list_database_names()
    print(f"TEST DB NAME: exists -> {MONGO_DB in existing_dbs} ({MONGO_DB})")

    db = client[MONGO_DB]
    col = db[MONGO_COLLECTION]

    if INIT_DB_AND_COLLECTION:
        # Insert a persistent document so the DB appears in Compass/Mongo Express
        # Use a stable _id so re-running doesn't create duplicates
        init_id = "_init_mongo_test"
        init_doc = {
            "_id": init_id,
            "kind": "init",
            "createdAt": datetime.now(timezone.utc),
            "note": "created by mongo_test.py so the db is visible in UIs",
        }
        res = col.update_one({"_id": init_id}, {"$setOnInsert": init_doc}, upsert=True)
        created = res.upserted_id is not None
        print(f"TEST DB COLLECTION: init doc present -> {not created} (created_now={created})")

    # verify collection list
    collections = db.list_collection_names()
    print(f"TEST DB COLLECTION: exists -> {MONGO_COLLECTION in collections} ({MONGO_COLLECTION})")
    print(f"TEST DB COLLECTION: all collections -> {collections}")

    # test query
    count = col.count_documents({})
    print(f"TEST DB COLLECTION: {MONGO_COLLECTION} count -> {count}")

    # show example doc
    sample = col.find_one({})
    print("TEST QUERY: sample doc ->", sample)

    print("OK mongo_test completed")


if __name__ == "__main__":
    main()