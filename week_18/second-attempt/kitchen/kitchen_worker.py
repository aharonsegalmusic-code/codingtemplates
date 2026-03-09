"""
Kitchen Worker Service

INPUT:
    - Kafka topic "pizza_orders" (consumes each order as JSON)

OUTPUT:
    - waits 15 seconds (simulates cooking time)
    - if order is not BURNT -> updates MongoDB status to "DELIVERED"
    - deletes the order's Redis cache key (forces fresh read on next API call)

FLOW:
    Kafka "pizza_orders" -> kitchen_worker -> sleep 15s
                                          -> MongoDB (status = DELIVERED)
                                          -> Redis (delete cached order)
"""

from .connection.kafka_connection_consumer import consumer
from .connection.mongo_connection import mongo
from .connection.redis_connection import r
import json
import time

import os
from dotenv import dotenv_values
ENV = {**dotenv_values(".env.local"), **os.environ}
TOPIC_ORDERS = ENV.get("TOPIC_ORDERS", "pizza_orders")

collection = mongo.collection("pizza_orders")
consumer.subscribe(TOPIC_ORDERS)


def kitchen():
    """
    Main consumer loop:
    1. poll kafka for new orders
    2. wait 15s (cooking time / gives enricher time to flag non-kosher)
    3. if not BURNT -> mark as DELIVERED
    4. delete redis cache so next API call gets fresh data
    """
    print("kitchen_worker running...")
    try:
        while True:
            order = consumer.poll(1.0)  # poll kafka with 1s timeout
            if order is None: continue
            if order.error():
                print(f"kitchen error: {order.error()}")
                continue

            order = json.loads(order.value())
            order_id = order["order_id"]
            print(type(order))
            print(order)

            # wait 15s - gives the enricher time to analyze and possibly mark BURNT
            time.sleep(15.0)

            # only mark DELIVERED if enricher didn't flag it as BURNT
            if order["status"] != "BURNT":
                collection.update_one(
                {"order_id": order_id},
                {"$set": {"status": "DELIVERED"}},
                )

            # invalidate redis cache for this order
            r.delete(order_id)

    finally:
        consumer.close()


kitchen()

# python -m kitchen.kitchen_worker
