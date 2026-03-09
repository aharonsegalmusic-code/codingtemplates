"""
Text Processor Service (Preprocessor)

INPUT:
    - Kafka topic "pizza_orders" (consumes each order as JSON)

OUTPUT:
    - updates MongoDB: sets allergies_flaged (bool) + protocol_cleaned (uppercase, no punctuation)
    - publishes cleaned data to Kafka topic "cleaned-instructions"
      with fields: order_id, pizza_type, special_instructions (cleaned), cleaned_prep

FLOW:
    Kafka "pizza_orders" -> text_worker -> MongoDB (update allergies + cleaned text)
                                        -> Kafka "cleaned-instructions" (publish cleaned data)
"""

from .connection.kafka_connection_consumer import consumer
from .connection.mongo_connection import mongo
from .clean_preprocessor import clean_instructions
import json
import re

import os
from dotenv import dotenv_values
ENV = {**dotenv_values(".env.local"), **os.environ}

TOPIC_ORDERS = ENV.get("TOPIC_ORDERS", "pizza_orders")

collection = mongo.collection("pizza_orders")
consumer.subscribe(TOPIC_ORDERS)

# =============================
#   +-----------------------+
#   |     processes         |
#   +-----------------------+

def allergy_label(order):
    """
    checks special_instructions for warning keywords ("allergy", "peanut", "gluten").
    if any found -> sets allergies_flaged=True in MongoDB.
    also cleans the text: removes punctuation, converts to UPPERCASE.
    returns the cleaned text for further processing.
    """
    text = order["special_instructions"].lower()
    # code words that trigger allergy flag
    codes = ["allergy", "peanut", "gluten"]
    allergies_flagged = any(code in text for code in codes)

    # clean: uppercase + remove punctuation
    upper_text = text.upper()
    cleaned_text = re.sub(r"[@#?$!().,]", "", upper_text)

    # update mongo with allergy flag and cleaned text
    collection.update_one(
            {"order_id": order["order_id"]},
            {"$set": {"allergies_flaged": allergies_flagged,
                        "protocol_cleaned": cleaned_text}}
            )
    return cleaned_text



#   +-----------------------+
#   |     main              |
#   +-----------------------+

def text_process():
    print("text_processor running...")
    try:
        while True:
            order = consumer.poll(1.0)
            if order is None: continue # validating you get an order and that it is not error
            if order.error():
                print(f"text error: {order.error()}")
                continue

            order = json.loads(order.value())
            clean_text = allergy_label(order)
            clean_instructions(order, clean_text)

    finally:
        consumer.close()

text_process()


# python -m text_processor.text_worker
