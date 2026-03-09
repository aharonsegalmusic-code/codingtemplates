# mongo_poll_new.py
import os
import json
import asyncio
from datetime import datetime

from motor.motor_asyncio import AsyncIOMotorClient


MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

MONGO_DB = os.getenv("MONGO_DB", "social_commerce")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "mini_users")  # change if needed

POLL_SECONDS = int(os.getenv("POLL_SECONDS", "10"))


def _jsonable(doc: dict) -> dict:
    doc = dict(doc)
    if "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return doc


async def main():
    client = AsyncIOMotorClient(MONGO_URI)
    col = client[MONGO_DB][MONGO_COLLECTION]

    last_time: datetime | None = datetime.min

    print(f"Polling Mongo every {POLL_SECONDS}s...")
    print(f"DB: {MONGO_DB} | Collection: {MONGO_COLLECTION}")

    while True:
        newest = await col.find_one(
            filter={"insertion_time": {"$exists": True}},
            sort=[("insertion_time", -1)],
            projection=None,
        )

        if newest is None:
            await asyncio.sleep(POLL_SECONDS)
            continue

        newest_time = newest.get("insertion_time")

        # First run: just set the checkpoint (don't print old data)
        if last_time is None:
            last_time = newest_time
            await asyncio.sleep(POLL_SECONDS)
            continue

        # If newest time changed -> fetch and print all docs newer than last_time
        if newest_time != last_time:
            cursor = col.find(
                {"insertion_time": {"$gt": last_time}},
                sort=[("insertion_time", 1)],
            )
            async for doc in cursor:
                print(json.dumps(_jsonable(doc), ensure_ascii=False, default=str))

            last_time = newest_time

        await asyncio.sleep(POLL_SECONDS)


if __name__ == "__main__":
    asyncio.run(main())