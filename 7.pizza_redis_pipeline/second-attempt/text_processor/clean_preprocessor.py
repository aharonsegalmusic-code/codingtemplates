"""
Text Processor - Clean Preprocessor (helper module)

INPUT:
    - order dict (from text_worker) + already-cleaned special_instructions text

OUTPUT:
    - looks up prep instructions from pizza_prep.json for the pizza_type
    - cleans prep text: removes punctuation, converts to UPPERCASE
    - publishes to Kafka topic "cleaned-instructions" with fields:
        order_id, pizza_type, special_instructions (cleaned), cleaned_prep

FLOW:
    text_worker calls clean_instructions() -> reads pizza_prep.json
                                           -> Kafka "cleaned-instructions"
"""

from .connection.mongo_connection import mongo
from .connection.kafka_connection_producer import producer
import json
import re

import os
from dotenv import dotenv_values
ENV = {**dotenv_values(".env.local"), **os.environ}

TOPIC_CLEAN_INST = ENV.get("TOPIC_CLEAN_INST", "cleaned-instructions")

collection = mongo.collection("pizza_orders")

def prep_extractor(pizza_type):
    """Reads pizza_prep.json and returns the prep instructions matching the pizza_type."""
    with open('data/pizza_prep.json', 'r') as file:
        prep = json.load(file)

    for pizza_name, instructions in prep.items():
        if pizza_type in pizza_name:
            return instructions
    return "No prep instructions available"


def clean_instructions(order,clean_text):
    """
    1. get special_instructions and prep method from pizza_prep.json
    2. clean both texts: remove punctuation, convert to UPPERCASE
    3. update mongo with cleaned texts
    """
    pizza_type = order["pizza_type"]
    prep_text = prep_extractor(pizza_type)

    cleaned_prep = re.sub(r"[@#?$!().,]", "", prep_text.upper())

    new_cleaned = {
        "order_id" : order["order_id"],
        "pizza_type" : pizza_type,
        "special_instructions" : clean_text,
        "cleaned_prep" :cleaned_prep
    }

    # send to kafka
    value = json.dumps(new_cleaned).encode('utf-8')
    # send is the class function that calls produce()
    producer.send(TOPIC_CLEAN_INST, value)
    producer.flush()
    return
