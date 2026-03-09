"""
API Router - File Upload & Order Lookup

ROUTES:
    POST /file_data/uploadfile  -> receives a JSON file of pizza orders
                                   saves each to MongoDB (status=PREPARING)
                                   publishes each to Kafka "pizza_orders"

    GET  /file_data/order/{id}  -> returns a single order by order_id
                                   cache-aside: checks Redis first (TTL 60s),
                                   falls back to MongoDB on cache miss

HELPERS:
    mongo_send()  -> validates with Pydantic, inserts orders into MongoDB
    kafka_send()  -> validates with Pydantic, publishes orders to Kafka
    redis_check() -> cache-aside pattern (Redis -> MongoDB fallback)
"""

from fastapi import APIRouter, File, UploadFile
from pydantic import BaseModel
from typing import List
import json
from .connection.kafka_connection_producer import producer

from .connection.mongo_connection import mongo
from .connection.redis_connection import r

import os
from dotenv import dotenv_values


ENV = {**dotenv_values(".env.local"), **os.environ}

TOPIC_ORDERS = ENV.get("TOPIC_ORDERS", "pizza_orders")

router = APIRouter(
    prefix="/file_data",
    tags=["file"],
)

# =============================
#   +-----------------------+
#   |    PYDANTIC MODEL     |
#   +-----------------------+

class Order(BaseModel):
    order_id: str
    pizza_type: str
    size: str
    quantity: int
    is_delivery: bool = False
    special_instructions: str = ""
    status: str = "PREPARING"


# =============================
#   +-----------------------+
#   |     HELPERS           |
#   +-----------------------+

def mongo_send(data):
    """
    for each record add "status" field
    set it to "PREPARING"
    insert one by one into mongo
    """
    collection = mongo.collection("pizza_orders")
    for order in data:
        current = Order(**order)
        collection.insert_one(current.model_dump())

    return {"count": len(data)}


def kafka_send(data):
    """
    send to kafka orders on by one
    """
    for order in data:
        current = Order(**order)
        value = json.dumps(current.model_dump()).encode('utf-8')
        # send is the class function that calls produce()
        producer.send(TOPIC_ORDERS, value)
        producer.flush()

    return {"count": len(data)}


def redis_check(order_id: str):
    """
    check if id in redis
    if is -> return it
    else -> extract from mongo and enter to redis and return it
    """

    redis_order = r.get(order_id)
    # if in redis
    if redis_order is not None:
        # convert redis(bits) to json
        redis_order = json.loads(redis_order)
        redis_order["source"] = "redis"
        return redis_order

    # if not in redis
    collection = mongo.collection("pizza_orders")
    mongo_order = collection.find_one({"order_id": order_id}, {"_id": 0})

    r.set(order_id, json.dumps(mongo_order), ex=60) # save in redis for 60 seconds
    # in response add source field
    mongo_order["source"] = "mongodb"
    return mongo_order


# =============================
#   +-----------------------+
#   |    ROUTES             |
#   +-----------------------+

@router.post("/uploadfile")
def post_file(file: UploadFile = File(...)):
    data = json.loads(file.file.read())

    mongo_response = mongo_send(data)
    kafka_response = kafka_send(data)

    return {"mongo response": mongo_response,
            "kafka response" : kafka_response}

@router.get("/order/{order_id}")
def get_by_id(order_id:str):
    order = redis_check(order_id)
    return order
