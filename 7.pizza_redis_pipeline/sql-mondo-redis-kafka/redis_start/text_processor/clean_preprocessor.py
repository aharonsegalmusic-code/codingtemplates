from .connection.mongo_connection import mongo
from .connection.kafka_connection_producer import producer
import json
import re

from dotenv import dotenv_values
ENV = dotenv_values(".env.local")

TOPIC_CLEAN_INST = ENV.get("TOPIC_CLEAN_INST", "cleaned-instructions")

collection = mongo.collection("pizza_orders")

def post_to_kafka_clean(data):
    pass

def prep_extractor(pizza_type):
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