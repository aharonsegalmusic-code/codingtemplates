from .connection.kafka_connection_consumer import consumer
from .connection.mongo_connection import mongo
from .connection.redis_connection import r
import json
import time

from dotenv import dotenv_values
ENV = dotenv_values(".env.local")
TOPIC_ORDERS = ENV.get("TOPIC_ORDERS", "pizza_orders")

collection = mongo.collection("pizza_orders")
consumer.subscribe(TOPIC_ORDERS)


def kitchen():
    print("running")
    try:
        while True:
            order = consumer.poll(1.0) 
            if order is None: continue
            if order.error():
                print(f"kitchen error: {order.error()}")
                continue

            order = json.loads(order.value())
            order_id = order["order_id"]
            print(type(order))
            print(order)


            # sleep to see in enricher makes it BURNT
            time.sleep(15.0)

            # this is can be seen as redundant but its for validation
            if order["status"] != "BURNT":
                collection.update_one(
                {"order_id": order_id},
                {"$set": {"status": "DELIVERED"}},
                )

            r.delete(order_id)

    finally:
        consumer.close()


kitchen()

# python -m kitchen.kitchen_worker