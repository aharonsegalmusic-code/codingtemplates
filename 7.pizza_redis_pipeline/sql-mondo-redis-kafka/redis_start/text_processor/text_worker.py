from .connection.kafka_connection_consumer import consumer
from .connection.mongo_connection import mongo
from .clean_preprocessor import clean_instructions
import json
import re

from dotenv import dotenv_values
ENV = dotenv_values(".env.local")

TOPIC_ORDERS = ENV.get("TOPIC_ORDERS", "pizza_orders")

collection = mongo.collection("pizza_orders")
consumer.subscribe(TOPIC_ORDERS)

# =============================
#   +-----------------------+
#   |     processes         |  
#   +-----------------------+

def allergy_label(order):
    """
    filter and label based on the code "allergy"
    """
    text = order["special_instructions"].lower()
    codes = ["allergy", "peanut", "gluten"]
    allergies_flagged = any(code in text for code in codes)

    upper_text = text.upper()
    cleaned_text = re.sub(r"[@#?$!().,]", "", upper_text)

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