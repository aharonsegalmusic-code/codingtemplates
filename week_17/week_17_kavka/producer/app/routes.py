import json
import os
import time
from typing import Any

from fastapi import APIRouter, Body, HTTPException

from .kafka_publisher import producer, ensure_topic_exists
from .mongo_connection import collection

router = APIRouter()
kafka_topic = os.getenv("KAFKA_TOPIC", "raw-records")


@router.get("/health")
def health():
    return {"status": "ok"}


@router.post("/records")
def records(payload=Body(...)):
    """
    Long-term fix:
    Accept either:
      - a single JSON object  { ... }
      - or a JSON list        [ { ... }, { ... } ]
    """
    if isinstance(payload, dict):
        docs = [payload]
    elif isinstance(payload, list):
        docs = payload
    else:
        raise HTTPException(status_code=400, detail="Payload must be a JSON object or a JSON list of objects")

    if len(docs) == 0:
        raise HTTPException(status_code=400, detail="Payload list is empty")

    result = collection.insert_many(docs)
    return {"inserted_count": len(result.inserted_ids)}


@router.post("/publish")
def publish(batch_size: int = 30, sleep_seconds: float = 0.5):
    if batch_size <= 0:
        raise HTTPException(status_code=400, detail="batch_size must be > 0")
    if sleep_seconds < 0:
        raise HTTPException(status_code=400, detail="sleep_seconds must be >= 0")

    # Ensure topic exists before producing (extra safety)
    ensure_topic_exists(kafka_topic)

    published = 0
    batch: list[dict[str, Any]] = []

    # projection removes _id so json.dumps works
    cursor = collection.find({}, projection={"_id": False}).batch_size(int(batch_size))

    for doc in cursor:
        batch.append(doc)
        if len(batch) >= batch_size:
            for item in batch:
                producer.produce(kafka_topic, value=json.dumps(item).encode("utf-8"))
                producer.poll(0)
                published += 1
                time.sleep(float(sleep_seconds))
            batch = []

    for item in batch:
        producer.produce(kafka_topic, value=json.dumps(item).encode("utf-8"))
        producer.poll(0)
        published += 1
        time.sleep(float(sleep_seconds))

    producer.flush(10)
    return {"published_count": published}